from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    user_role = models.CharField(max_length=12, choices=UserRoles.choices, default=UserRoles.MEMBER)

    phone = models.EmailField(max_length=40,verbose_name='номер телефона', null=True, blank=True)
    avatar = models.ImageField(upload_to='media/users/', verbose_name='аватар', null=True, blank=True)
    city = models.CharField(verbose_name='город', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []