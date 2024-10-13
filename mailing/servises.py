from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from mailing.models import Mailing, MailingLog


def check_periodicity_mail_start(mail):
    """проверяет наступление условия отправки рассылки"""

    mail_time_start = mail.time_start
    mail_time_end = mail.time_end
    mail_day = mail.day
    mail_day_week = mail.day_week

    if mail_time_start > datetime.now().time() > mail_time_end:
        return True
    elif mail_day == datetime.now().day:
        return True
    elif mail_day_week == str(datetime.now().weekday()):
        return True
    else:
        return False


def mail_send(mail, client):
    """отправляет письма пользователям из рассылки по расписанию"""

    mail_send_ = send_mail(
        mail.name,
        mail.body,
        settings.EMAIL_HOST_USER,
        [client.email],
    )

    return mail_send_


def mail_status_chenge():
    """меняет статус рассылки 'запущена' на 'создана' после времени окончания рассылки"""
    mailing = Mailing.objects.filter(is_active=True)
    mailinglog = MailingLog.objects.all()

    for mail in mailing:
        maillog = mailinglog.filter(mailing_current=mail).all().order_by('-time_try').first()
        if mail.status == 'created' and mail.time_end.hour > datetime.now().hour:
            mail.status = 'created'
            mail.save()
        elif mail.status == 'created' and maillog is not None and datetime.now().day > maillog.time_try.day():
            mail.status = 'created'
            mail.save()