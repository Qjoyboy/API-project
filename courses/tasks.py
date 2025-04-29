from datetime import timedelta, datetime

from celery import shared_task
from django.core.mail import send_mail
from rest_framework.fields import DateField

from courses.models import Course
from users.models import User


@shared_task
def send_email_of_update():
    send_mail(
        subject="Курс обновлен",
        message=f"Обновление курса прибыло",
        from_email="admin@admin",
        recipient_list=["first@email.com"],
        fail_silently=False
    )

@shared_task
def users_active_check(pk):
    user = User.objects.get(pk=pk)
    now = datetime.now()
    last_login_user = user.last_login
    res = now - last_login_user
    if res > timedelta(30):
        user.is_active = False