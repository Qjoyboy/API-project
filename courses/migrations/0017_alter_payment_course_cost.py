# Generated by Django 5.1.6 on 2025-02-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_alter_course_url_alter_lesson_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='course_cost',
            field=models.IntegerField(default=10000, verbose_name='сумма оплаты'),
        ),
    ]
