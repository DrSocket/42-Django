"""Admin registrations. The default admin application is kept, as required."""

from django.contrib import admin

from .models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "created")
    list_display_links = ("id",)
    list_filter = ("room", "user")
    readonly_fields = ("created",)
    search_fields = ("body", "user__username")
    date_hierarchy = "created"
