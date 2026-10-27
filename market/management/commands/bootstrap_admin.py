import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial Django superuser from environment variables if it does not exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not (username and email and password):
            self.stdout.write(
                self.style.WARNING(
                    "Initial admin not created: set DJANGO_SUPERUSER_USERNAME, "
                    "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD in the host environment."
                )
            )
            return

        User = get_user_model()
        existing = User.objects.filter(username=username).first()
        if existing:
            if existing.is_superuser and existing.is_staff:
                self.stdout.write("Initial admin already exists; no account credentials were changed.")
                return
            raise CommandError(
                f"The username {username!r} already exists but is not a superuser. "
                "Choose a different DJANGO_SUPERUSER_USERNAME or review that account manually."
            )

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Initial Django superuser {username!r} created."))
