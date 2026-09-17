"""
Models for ex01-ex04.

The subject requires the chatroom names to live in the database, so Room is the
"suitable model" it asks for. Message stores the history that ex02 replays.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse


class Room(models.Model):
    """A chatroom. Its name is what the subject requires to be in database."""

    name = models.CharField("name", max_length=64, unique=True)
    slug = models.SlugField("slug", max_length=64, unique=True)

    class Meta:
        verbose_name = "room"
        verbose_name_plural = "rooms"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chat:room", kwargs={"slug": self.slug})

    @property
    def group_name(self):
        """Name of the channel-layer group that broadcasts to this room."""
        return f"chat.{self.slug}"


class Message(models.Model):
    """One message posted in a room by a user."""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="room",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name="user",
    )
    body = models.TextField("body")
    created = models.DateTimeField("created", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "messages"
        # Ascending, because the subject requires messages to be displayed
        # oldest-first and never to change order. `id` breaks ties so that two
        # messages sharing a timestamp keep a stable, insertion-ordered result.
        ordering = ("created", "id")

    def __str__(self):
        return f"{self.user}: {self.body[:40]}"
