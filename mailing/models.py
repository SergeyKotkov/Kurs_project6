from datetime import datetime
from django.db import models
from config import settings
from mailing.utils import NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='электронная почта', unique=True)
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.email}  {self.fio}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    CHOICES_STATUS = (
        ('created', 'создана'),
        ('running', 'запущена'),
        ('completed', 'завершена'),
    )
    CHOICES_TIME = (
        ('day', 'раз в день'),
        ('week', 'раз в неделю'),
        ('mon', 'раз в месяц'),
    )
    CHOICES_DAYWEEK = (
        ('0', 'понедельник'),
        ('1', 'вторник'),
        ('2', 'среда'),
        ('3', 'четверг'),
        ('4', 'пятница'),
        ('5', 'суббота'),
        ('6', 'вскресенье'),
    )

    name = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, verbose_name='статус', default='created')
    time_start = models.TimeField(verbose_name='начало времени отправки',
                                  help_text='Введите время в формате ЧЧ:ММ через двоеточие. Начало времени отправки '
                                            'должно быть раньше окончания времени отправки ')
    time_end = models.TimeField(verbose_name='окончание времени отправки',
                                help_text='Введите время в формате ЧЧ:ММ через  двоеточие. Начало времени отправки '
                                            'должно быть раньше окончания времени отправки ')
    periodicity = models.CharField(max_length=20, choices=CHOICES_TIME, verbose_name='периодичность')
    day = models.IntegerField(verbose_name='день', **NULLABLE,
                              help_text='Введите число при периодичности раз в месяц. Число должно быть от 1 до 31')
    day_week = models.CharField(max_length=15, choices=CHOICES_DAYWEEK, verbose_name='день недели', **NULLABLE,
                                help_text='Выберите день недели при периодичности раз в неделю')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность рассылки')
    clients = models.ManyToManyField("Client", related_name='clients', verbose_name='клиенты')

    def __str__(self):
        return f'{self.name}, {self.body}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        ordering = ['name', ]


class MailingLog(models.Model):
    STATUS_CHOICES = (
        ('1', 'Успешно'),
        ('0', 'Неуспешно'),
    )

    time_try = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    client = models.CharField(max_length=150, verbose_name='клиент', **NULLABLE)
    mailing_current = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Лог: "{self.mailing_current}"'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['-time_try', ]