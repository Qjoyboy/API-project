from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='media/preview/', null=True, blank=True)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural='Курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(upload_to='media/preview/', null=True, blank=True)
    description = models.TextField(verbose_name='описание урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson', null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.course.title} - {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Payment(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE,related_name='payment')
    pay_date = models.DateField(default='2000-12-01',verbose_name='время')
    bought_course = models.CharField(max_length=100, verbose_name='оплаченный курс')
    course_cost = models.IntegerField(verbose_name='сумма оплаты')
    PAYMENT_METHOD = [
        ("card", "card"),
        ("cash", "cash"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, default='card')