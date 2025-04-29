from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        mods_list = [
            {'email': 'mod1@email.com', 'password':'123','is_staff': True, 'city': 'Moscow', 'phone': '8777-7777777',
             'avatar': None},
            {'email': 'mod2@email.com','password':'123', 'is_staff': True, 'city': 'Los-Angeles', 'phone': '8-111-111-11-11',
             'avatar': None}
        ]

        mods_for_create = []
        for mods_item in mods_list:
            mods_for_create.append(
                User(**mods_item)
            )
        print(mods_for_create)