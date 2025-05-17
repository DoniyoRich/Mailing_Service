from django.conf import settings
from django.db import models

from mailing.constants import MAILING_ATTEMPT_STATUS, MAILING_STATUS


# Модель Получателя рассылки
class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="e-mail Получателя")
    fullname = models.CharField(max_length=100, verbose_name="ФИО Получателя")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        related_name="recipients",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["fullname"]

    def __str__(self):
        return self.fullname


# Модель Сообщения
class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема письма", blank=True, null=True)
    message_body = models.TextField(verbose_name="Текст письма", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        related_name="messages",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]

    def __str__(self):
        return self.subject[:30]


# Модель Рассылки
class Mailing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Рассылка создана: ")
    sent_at = models.DateTimeField(verbose_name="Рассылка отправлена: ")
    finished_at = models.DateTimeField(verbose_name="Рассылка завершена: ")
    status = models.CharField(choices=MAILING_STATUS, verbose_name="Статус рассылки: ")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        related_name="mailings",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ('can_switch_off_mailing', 'Может отключить рассылку'),
        ]


# Модель Попытка рассылки
class MailingAttempt(models.Model):
    attempt_date = models.DateTimeField()
    attempt_status = models.CharField(choices=MAILING_ATTEMPT_STATUS, verbose_name="Статус попытки: ")
    mail_server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
