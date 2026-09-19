"""
ASGI config for the d09 project.

It routes plain HTTP to Django's usual application and WebSocket connections to
the chat consumers used by ex01-ex04.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d09.settings")

# Initialise Django before importing anything that touches the app registry:
# chat.routing imports the consumer, which imports models.
django_asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

import chat.routing  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        # AuthMiddlewareStack populates scope["user"] from the session cookie,
        # which is how the consumer enforces "logged-in users only".
        "websocket": AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
        ),
    }
)
