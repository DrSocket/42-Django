"""WebSocket URL patterns for the chat application."""

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<slug>[-\w]+)/$", consumers.ChatConsumer.as_asgi()),
]
