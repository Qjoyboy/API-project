from django.core.management import BaseCommand

from courses.models import Payment
from users.models import User


class Command(BaseCommand):
    def handle(self,*args, **options):
        courses_list = [
            {'email': 'first@email.com', 'pay_date': '2020-08-01', 'bought_course': 1, 'course_cost': 20000,'payment_method': "cash"},
            {'email': 'second@email.com', 'pay_date': '2020-07-01', 'bought_course': 3, 'course_cost': 30000,'payment_method': "card"},
            {'email': 'third@email.com', 'pay_date': '2020-06-01', 'bought_course': 4, 'course_cost': 40000,'payment_method': "card"}
        ]

        courses_for_create = []
        for course_item in courses_list:
            user = User.objects.get_or_create(email=course_item['email'])[0]
            course_item['email'] = user
            courses_for_create.append(
                Payment(**course_item)
            )
        print(courses_for_create)
        Payment.objects.bulk_create(courses_for_create)