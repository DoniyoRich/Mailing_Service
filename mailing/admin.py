from django.contrib import admin

from .models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "fullname")
    list_filter = ("email", "fullname")
    search_fields = ("email", "fullname")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "message_body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("sent_at", "finished_at", "status",)
    list_filter = ("sent_at", "finished_at", "status",)
    search_fields = ("sent_at", "finished_at", "status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("attempt_date", "attempt_status")
    list_filter = ("attempt_date", "attempt_status")
    search_fields = ("attempt_date", "attempt_status")
