from datetime import datetime
from django.core.management import BaseCommand
from mailing.models import Mailing, MailingLog
from mailing.services import mail_send


class Command(BaseCommand):
    """Немедленный запуск всех активных рассылок"""

    def handle(self, *args, **options):

        mailing = Mailing.objects.filter(is_active=True)

        for mail in mailing:
            clients = mail.clients.all()
            if clients is None:
                log = MailingLog.objects.create(
                    time_try=datetime.now(),
                    status='Неудачно',
                    mailing_current=mail,
                    server_response='Нет клиентов в рассылке',
                    user=mail.user,
                )
                log.save()
                continue
            else:
                for client in clients:
                    try:
                        mail_send(mail, client)
                    except ConnectionRefusedError as error:
                        log = MailingLog.objects.create(
                            time_try=datetime.now(),
                            status='Неудачно',
                            mailing_current=mail,
                            server_response=error,
                            client=client.email,
                            user=mail.user,
                        )
                        log.save()
                    else:
                        log = MailingLog.objects.create(
                            time_try=datetime.now(),
                            status='Успешно',
                            mailing_current=mail,
                            client=client.email,
                            user=mail.user,
                        )
                        log.save()
                        mail.save()