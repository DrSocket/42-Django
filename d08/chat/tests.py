"""Tests for ex01-ex04: rooms, WebSocket chat, history and the user list."""

from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from . import consumers
from .models import Message, Room
from .routing import websocket_urlpatterns


class RoomModelTests(TestCase):
    """ex01: the room names must live in the database."""

    def test_the_three_rooms_are_seeded_by_migration(self):
        self.assertEqual(Room.objects.count(), 3)
        self.assertEqual(
            sorted(Room.objects.values_list("slug", flat=True)),
            ["general", "random", "support"],
        )

    def test_messages_are_ordered_oldest_first(self):
        room = Room.objects.get(slug="general")
        user = User.objects.create_user(username="alice", password="s3cret-pass")
        first = Message.objects.create(room=room, user=user, body="first")
        second = Message.objects.create(room=room, user=user, body="second")
        self.assertEqual(list(room.messages.all()), [first, second])


class RoomViewTests(TestCase):
    """ex01: three links, and the chat is for logged-in users only."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="s3cret-pass")

    def test_room_index_requires_login(self):
        response = self.client.get(reverse("chat:rooms"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/account", response["Location"])

    def test_room_page_requires_login(self):
        response = self.client.get(reverse("chat:room", kwargs={"slug": "general"}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/account", response["Location"])

    def test_room_index_lists_a_link_per_room(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat:rooms"))
        self.assertEqual(response.status_code, 200)
        for room in Room.objects.all():
            self.assertContains(response, room.get_absolute_url())

    def test_room_page_shows_the_chat_name_and_both_containers(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat:room", kwargs={"slug": "general"}))
        self.assertContains(response, "General")
        self.assertContains(response, 'id="messages"')
        self.assertContains(response, 'id="users"')

    def test_unknown_room_is_404(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat:room", kwargs={"slug": "nope"}))
        self.assertEqual(response.status_code, 404)


def _communicator(user, slug="general"):
    """A WebSocket client for `slug`, authenticated as `user`."""
    communicator = WebsocketCommunicator(
        URLRouter(websocket_urlpatterns), f"/ws/chat/{slug}/"
    )
    # AuthMiddlewareStack is what populates this in the running server; the
    # tests inject it directly so they exercise the consumer, not the session.
    communicator.scope["user"] = user
    return communicator


async def _drain(communicator):
    """Collect everything already queued for a socket."""
    received = []
    while True:
        if await communicator.receive_nothing(timeout=0.15):
            return received
        received.append(await communicator.receive_json_from())


class ChatConsumerTests(TransactionTestCase):
    """The WebSocket behaviour required by ex01-ex03."""

    def setUp(self):
        # The connected-user registry is module state; keep tests independent.
        consumers._CONNECTED.clear()
        # TransactionTestCase flushes between tests, so the room seeded by the
        # data migration may or may not still be present.
        self.room, _ = Room.objects.get_or_create(
            slug="general", defaults={"name": "General"}
        )
        self.alice = User.objects.create_user(username="alice", password="s3cret-pass")
        self.bob = User.objects.create_user(username="bob", password="s3cret-pass")

    def tearDown(self):
        consumers._CONNECTED.clear()

    async def test_anonymous_connection_is_refused(self):
        from django.contrib.auth.models import AnonymousUser

        communicator = _communicator(AnonymousUser())
        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_connection_to_unknown_room_is_refused(self):
        communicator = _communicator(self.alice, slug="does-not-exist")
        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_joining_announces_the_arrival_to_the_joiner(self):
        communicator = _communicator(self.alice)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        events = await _drain(communicator)
        joins = [e for e in events if e["type"] == "join"]
        self.assertEqual([e["username"] for e in joins], ["alice"])

        await communicator.disconnect()

    async def test_join_is_broadcast_to_everyone_in_the_room(self):
        alice = _communicator(self.alice)
        await alice.connect()
        await _drain(alice)

        bob = _communicator(self.bob)
        await bob.connect()

        # Alice must be told that bob arrived...
        alice_events = await _drain(alice)
        self.assertIn(
            {"type": "join", "username": "bob"},
            alice_events,
        )
        # ...and bob must see his own arrival too.
        bob_events = await _drain(bob)
        self.assertIn({"type": "join", "username": "bob"}, bob_events)

        await alice.disconnect()
        await bob.disconnect()

    async def test_a_message_reaches_every_member_and_is_stored(self):
        alice = _communicator(self.alice)
        bob = _communicator(self.bob)
        await alice.connect()
        await bob.connect()
        await _drain(alice)
        await _drain(bob)

        await alice.send_json_to({"body": "hello room"})

        expected = {
            "type": "message",
            "username": "alice",
            "body": "hello room",
            "history": False,
        }
        self.assertIn(expected, await _drain(alice))
        self.assertIn(expected, await _drain(bob))

        await alice.disconnect()
        await bob.disconnect()

        from channels.db import database_sync_to_async

        bodies = await database_sync_to_async(
            lambda: list(self.room.messages.values_list("body", flat=True))
        )()
        self.assertEqual(bodies, ["hello room"])

    async def test_blank_messages_are_ignored(self):
        alice = _communicator(self.alice)
        await alice.connect()
        await _drain(alice)

        await alice.send_json_to({"body": "   "})
        self.assertTrue(await alice.receive_nothing(timeout=0.2))

        await alice.disconnect()

    async def test_history_replays_the_last_three_messages_oldest_first(self):
        """ex02."""
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def seed():
            for body in ["m1", "m2", "m3", "m4"]:
                Message.objects.create(room=self.room, user=self.bob, body=body)

        await seed()

        alice = _communicator(self.alice)
        await alice.connect()
        events = await _drain(alice)

        history = [e for e in events if e["type"] == "message" and e["history"]]
        self.assertEqual([e["body"] for e in history], ["m2", "m3", "m4"])

        await alice.disconnect()

    async def test_user_list_tracks_joins_and_leaves(self):
        """ex03."""
        alice = _communicator(self.alice)
        await alice.connect()

        lists = [e["users"] for e in await _drain(alice) if e["type"] == "users"]
        self.assertEqual(lists[-1], ["alice"])

        bob = _communicator(self.bob)
        await bob.connect()

        lists = [e["users"] for e in await _drain(alice) if e["type"] == "users"]
        self.assertEqual(lists[-1], ["alice", "bob"])

        await bob.disconnect()

        events = await _drain(alice)
        self.assertIn({"type": "leave", "username": "bob"}, events)
        lists = [e["users"] for e in events if e["type"] == "users"]
        self.assertEqual(lists[-1], ["alice"])

        await alice.disconnect()

    async def test_a_second_tab_does_not_duplicate_or_drop_the_user(self):
        """Two connections for one user: one entry, and no premature 'has left'."""
        first = _communicator(self.alice)
        second = _communicator(self.alice)
        await first.connect()
        await _drain(first)
        await second.connect()

        events = await _drain(first)
        lists = [e["users"] for e in events if e["type"] == "users"]
        self.assertEqual(lists[-1], ["alice"])
        # No second "alice has joined" for the same user.
        self.assertNotIn({"type": "join", "username": "alice"}, events)

        # Closing one tab must not announce a departure.
        await second.disconnect()
        events = await _drain(first)
        self.assertNotIn({"type": "leave", "username": "alice"}, events)

        await first.disconnect()
