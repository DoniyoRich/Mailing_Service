from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL
from mailing.models import Mailing, MailingAttempt


class Command(BaseCommand):
    """
    Команда для ручной отправки рассылки из командной строки.
    Пример использования:
    python manage.py send_mailing 50
    - где 50 - ID рассылки
    """
    help = 'Ручная отправка рассылки по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена'))
            return

        self.stdout.write(f'Начата отправка рассылки "{mailing.message.subject}"...')

        mailing.status = 'Запущена'
        mailing.sent_at = timezone.now()
        mailing.save()

        recipients = mailing.recipient.all()
        total = recipients.count()
        success = 0

        for recipient in recipients:
            attempt = MailingAttempt(
                mailing=mailing,
                recipient_email=recipient,
                owner=mailing.owner,
                attempt_date=timezone.now()
            )

            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.message_body,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False
                )
                attempt.attempt_status = 'Успешно'
                attempt.mail_server_response = 'Доставлено'
                success += 1
                self.stdout.write(self.style.SUCCESS(f'Успешно: {recipient.email}'))
            except Exception as e:
                attempt.attempt_status = 'Ошибка'
                attempt.mail_server_response = str(e)[:255]
                self.stdout.write(self.style.ERROR(f'Ошибка: {recipient.email} - {str(e)}'))
            finally:
                attempt.save()

        mailing.finished_at = timezone.now()
        mailing.status = 'Завершена' if success == total else 'Ошибки'
        mailing.save()

        self.stdout.write(self.style.SUCCESS(
            f'Завершено. Успешно: {success}/{total}'
        ))
