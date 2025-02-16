from django.db import models

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='урок')
    title = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(upload_to='media/preview/', null=True, blank=True)
    description = models.TextField(verbose_name='описание урока')
    url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.course.title} - {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'