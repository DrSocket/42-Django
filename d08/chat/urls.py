"""URLs for the chat application."""

from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("chat/", views.rooms, name="rooms"),
    path("chat/<slug:slug>/", views.room, name="room"),
]
