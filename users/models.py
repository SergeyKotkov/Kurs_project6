import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.utils import NULLABLE

default_code = ''.join([str(random.randint(0, 9)) for _ in range(12)])


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность пользователя',)
    email_verified = models.BooleanField(default=False, verbose_name='верификация почты')
    ver_code = models.CharField(max_length=15, default=default_code, verbose_name='код из письма')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'