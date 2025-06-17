from django.core.management import BaseCommand, CommandError
from apps.users.models import User


class Command(BaseCommand):
    help = "Make the user with the given email active"

    def add_arguments(self, parser) -> None:
        parser.add_argument("email", type=str, help="user email")

    def handle(self, *args, **options) -> None:
        email = options.get("email")

        if not email:
            raise CommandError("Error: Email is required")

        user = User.objects.filter(email=email).first()

        if not user:
            raise CommandError(f"Error: User with {email} dose not exists")

        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS("User activated successfully"))
