from datetime import datetime
from django.core.management import BaseCommand
from mailing.models import Mailing, MailingLog
from mailing.services import check_periodicity_mail_start, mail_send


class Command(BaseCommand):
    def handle(self, *args, **options):

        mailing = Mailing.objects.filter(is_active=True)

        for mail in mailing:
            check_periodicity_mail_start_ = check_periodicity_mail_start(mail)

            if check_periodicity_mail_start_ and mail.status == 'created':
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
                            mail.status = 'running'
                            mail.save()