# Generated by Django 5.1.6 on 2025-02-25 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_payment_course_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='bought_course',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='оплаченный курс'),
        ),
    ]
