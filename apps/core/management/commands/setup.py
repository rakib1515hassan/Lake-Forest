from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Setup the project'

    def handle(self, *args, **options):
        user = User()

        user.first_name = "Admin"
        user.last_name = "Admin"
        user.email = "admin@admin.com"
        user.is_superuser = True
        user.save()

        user.set_password("@admin123")
        user.save()

        self.stdout.write(self.style.SUCCESS("Admin user created"))





