"""
A `manage.py` command to create a login user without opening the admin site.

The accounts used by the AJAX login page (ex00) and the chat (ex01+) are plain
Django users. Django ships `createsuperuser` but has no built-in command for a
*normal* user, so this fills that gap for demos and evaluation.

    python manage.py createuser alice                 # prompts for a password
    python manage.py createuser alice --password pw   # non-interactive
    python manage.py createuser boss --admin          # a superuser instead

The password is asked twice (hidden) when --password is not given.
"""

from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a login user (a normal user by default, or a superuser with --admin)."

    def add_arguments(self, parser):
        parser.add_argument("username", help="The name the person logs in with.")
        parser.add_argument(
            "--password",
            help="Set the password directly (otherwise you are prompted for it).",
        )
        parser.add_argument(
            "--admin",
            action="store_true",
            help="Create a superuser (can open /admin/) instead of a normal user.",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        username = options["username"].strip()
        if not username:
            raise CommandError("The username cannot be empty.")
        if User.objects.filter(username=username).exists():
            raise CommandError(f"A user named {username!r} already exists.")

        password = options["password"]
        if not password:
            password = getpass("Password: ")
            if password != getpass("Password (again): "):
                raise CommandError("The two passwords did not match.")
        if not password:
            raise CommandError("The password cannot be empty.")

        if options["admin"]:
            User.objects.create_superuser(username=username, password=password)
            kind = "superuser"
        else:
            User.objects.create_user(username=username, password=password)
            kind = "user"

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {kind} {username!r}. They can now log in at /account."
            )
        )
