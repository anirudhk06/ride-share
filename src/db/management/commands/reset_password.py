import getpass
from django.contrib.auth.password_validation import validate_password
from django.core.management import BaseCommand, CommandError
from apps.users.models import User


class Command(BaseCommand):
    help = "Reset password of the user with the given email"

    def add_arguments(self, parser) -> None:
        parser.add_argument("email", type=str, help="user email")

    def handle(self, *args, **options) -> None:
        email = options.get("email")

        if not email:
            self.stderr.write("Error: Email is required")
            return

        user = User.objects.filter(email=email).first()

        if not user:
            self.stderr.write(f"Error: User with {email} dose not exists")
            return

        password: str = getpass.getpass("Password: ")
        confirm_password: str = getpass.getpass("Password (again): ")

        if password != confirm_password:
            self.stderr.write("Error: Your password didn't match.")
            return

        if password.strip() == "":
            self.stderr.write("Error: Blank password aren't allowed.")
            return

        try:
            validate_password(password, user)
        except Exception as e:
            raise CommandError(e)

        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS("User password updated successfully"))
