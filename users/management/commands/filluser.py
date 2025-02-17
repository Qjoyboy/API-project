from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_list = [
            {'email':'first@email.com','city':'Moscow','phone':'8999-999-99-99','avatar':None},
            {'email': 'second@email.com', 'city': 'Los-Angeles', 'phone': '8-222-222-22-22', 'avatar': None},
            {'email': 'third@email.com', 'city': 'California', 'phone': '8-888-888-88-88', 'avatar': None}
        ]

        users_for_create = []
        for users_item in users_list:
            users_for_create.append(
                User(**users_item)
            )
        print(users_for_create)