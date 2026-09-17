"""
WebSocket consumer for ex01-ex03.

One channel-layer group per room, so a message is broadcast to exactly the
users who joined that room. Connected users are tracked per room in
`_CONNECTED`; the in-memory channel layer already confines the project to a
single process, so a module-level dict is the right scope for that state.
"""

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from .models import Message, Room

# {room_slug: {channel_name: username}}
#
# Keyed by channel rather than by username so that the same user opening two
# tabs is two entries, and closing one tab does not remove them from the list.
_CONNECTED = {}


def _add_connection(slug, channel_name, username):
    """Register a connection. Returns True if the user was not already here."""
    room_members = _CONNECTED.setdefault(slug, {})
    was_present = username in room_members.values()
    room_members[channel_name] = username
    return not was_present


def _remove_connection(slug, channel_name):
    """Drop a connection. Returns True if that was the user's last one."""
    room_members = _CONNECTED.get(slug, {})
    username = room_members.pop(channel_name, None)
    if username is None:
        return False
    if not room_members:
        _CONNECTED.pop(slug, None)
    return username not in room_members.values()


def _usernames(slug):
    """Connected usernames in a room, deduplicated and sorted for display."""
    return sorted(set(_CONNECTED.get(slug, {}).values()))


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Handles one user's connection to one room."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.slug = None
        self.username = None

    # -- connection lifecycle ------------------------------------------------

    async def connect(self):
        user = self.scope.get("user")

        # The chat is only available to logged-in users.
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.room = await self._get_room(self.slug)

        # Refuse to open a socket for a room that does not exist.
        if self.room is None:
            await self.close(code=4404)
            return

        self.username = user.get_username()

        await self.channel_layer.group_add(self.room.group_name, self.channel_name)
        await self.accept()

        # ex02: replay the last few messages to this socket alone, oldest
        # first, before announcing the arrival.
        for message in await self._recent_messages(self.room):
            await self.send_json(
                {
                    "type": "message",
                    "username": message["username"],
                    "body": message["body"],
                    "history": True,
                }
            )

        is_new = _add_connection(self.slug, self.channel_name, self.username)

        # ex01: the join notice must reach everyone, including the joiner.
        # ex03: and the user list must update for everyone.
        if is_new:
            await self.channel_layer.group_send(
                self.room.group_name,
                {"type": "chat.join", "username": self.username},
            )
        await self._broadcast_users()

    async def disconnect(self, code):
        # connect() may have closed before joining a group.
        if self.room is None or self.username is None:
            return

        was_last = _remove_connection(self.slug, self.channel_name)

        await self.channel_layer.group_discard(
            self.room.group_name, self.channel_name
        )

        # ex03: announce the departure and refresh everyone's user list.
        if was_last:
            await self.channel_layer.group_send(
                self.room.group_name,
                {"type": "chat.leave", "username": self.username},
            )
        await self._broadcast_users()

    # -- inbound ------------------------------------------------------------

    async def receive_json(self, content, **kwargs):
        """A message posted by this user."""
        if self.room is None or self.username is None:
            return

        body = (content or {}).get("body", "")
        if not isinstance(body, str):
            return

        body = body.strip()
        if not body:
            return

        await self._save_message(self.room, self.scope["user"], body)

        # Broadcast to the room, which includes this socket.
        await self.channel_layer.group_send(
            self.room.group_name,
            {"type": "chat.message", "username": self.username, "body": body},
        )

    # -- group event handlers ----------------------------------------------

    async def chat_message(self, event):
        await self.send_json(
            {
                "type": "message",
                "username": event["username"],
                "body": event["body"],
                "history": False,
            }
        )

    async def chat_join(self, event):
        await self.send_json({"type": "join", "username": event["username"]})

    async def chat_leave(self, event):
        await self.send_json({"type": "leave", "username": event["username"]})

    async def chat_users(self, event):
        await self.send_json({"type": "users", "users": event["users"]})

    # -- helpers ------------------------------------------------------------

    async def _broadcast_users(self):
        await self.channel_layer.group_send(
            self.room.group_name,
            {"type": "chat.users", "users": _usernames(self.slug)},
        )

    @database_sync_to_async
    def _get_room(self, slug):
        return Room.objects.filter(slug=slug).first()

    @database_sync_to_async
    def _recent_messages(self, room):
        """The last CHAT_HISTORY_SIZE messages of a room, oldest first."""
        limit = getattr(settings, "CHAT_HISTORY_SIZE", 3)
        newest_first = room.messages.select_related("user").order_by(
            "-created", "-id"
        )[:limit]
        return [
            {"username": message.user.get_username(), "body": message.body}
            for message in reversed(list(newest_first))
        ]

    @database_sync_to_async
    def _save_message(self, room, user, body):
        return Message.objects.create(room=room, user=user, body=body)
