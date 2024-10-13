from django.db import models

from config import settings
from mailing.utils import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(verbose_name='изображение', **NULLABLE)
    date_of_creation = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
