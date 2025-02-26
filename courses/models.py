from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='media/preview/', null=True, blank=True)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=250,default='https://youtube.com/')
    amount = models.IntegerField(default=10000, verbose_name='цена курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural='Курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(upload_to='media/preview/', null=True, blank=True)
    description = models.TextField(verbose_name='описание урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    url = models.URLField(max_length=250,default='https://youtube.com/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.course.title} - {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Payment(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE,related_name='payment')
    pay_date = models.DateField(default='2000-12-01',verbose_name='время', null=True, blank=True)
    bought_course = models.CharField(max_length=100, verbose_name='оплаченный курс', null=True, blank=True)
    course_bought = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(verbose_name='сумма оплаты', default=10000)
    PAYMENT_METHOD = [
        ("card", "card"),
        ("cash", "cash"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, default='card')
    session_id = models.CharField(max_length=150, verbose_name='id сессии', null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')


class Subscribe(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_sub')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_sub', null=True, blank=True)