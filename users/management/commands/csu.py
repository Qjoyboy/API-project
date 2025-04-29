from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin1@admin.com",
        )
        user.set_password("123")
        user.is_superuser = True
        user.user_role = "moderator"
        user.is_staff = True
        user.save()