"""
Seed the three chatrooms ex01 asks for.

The room names have to come from the database, so they are created by a data
migration: `manage.py migrate` alone is enough to get a working project.
"""

from django.db import migrations

DEFAULT_ROOMS = [
    ("General", "general"),
    ("Random", "random"),
    ("Support", "support"),
]


def create_rooms(apps, schema_editor):
    Room = apps.get_model("chat", "Room")
    for name, slug in DEFAULT_ROOMS:
        Room.objects.get_or_create(slug=slug, defaults={"name": name})


def delete_rooms(apps, schema_editor):
    Room = apps.get_model("chat", "Room")
    Room.objects.filter(slug__in=[slug for _, slug in DEFAULT_ROOMS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_rooms, delete_rooms),
    ]
