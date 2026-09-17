"""Views for ex01: the room index and one page per chatroom."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Room


@login_required
def rooms(request):
    """Index listing one link per chatroom."""
    return render(request, "chat/rooms.html", {"rooms": Room.objects.all()})


@login_required
def room(request, slug):
    """A single chatroom page."""
    return render(request, "chat/room.html", {"room": get_object_or_404(Room, slug=slug)})
