from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.models import Mailing, Recipient, Message


# -----------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С РАССЫЛКАМИ
# -----------------------------------------

class MailingsTotalList(ListView):
    """
    Класс отображения списка всех рассылок в системе.
    """
    model = Mailing
    template_name = "mailings/mailings.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total"] = 100
        context["total_active"] = 50
        context["unique_recipients"] = 7

        return context


class SearchResults(ListView):
    """
    Класс отображения результатов поиска рассылок.
    """
    model = Mailing
    template_name = "mailings/search_results.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_found"] = "20"
        context["total_active"] = 10

        return context


class UserMailingsList(ListView, PermissionRequiredMixin):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "mailing"


class AddMailing(CreateView, PermissionRequiredMixin):
    """
    Класс добавления рассылки.
    """
    model = Mailing
    template_name = "mailings/add_mailing.html"
    context_object_name = "mailing"


class DetailMailing(DetailView, PermissionRequiredMixin):
    """
    Класс просмотра детальной информации конкретной рассылки.
    """
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"


class UpdateMailing(UpdateView, PermissionRequiredMixin):
    """
    Класс редактирования рассылки.
    """
    model = Mailing
    template_name = "mailings/update_mailing.html"
    context_object_name = "mailing"


class DeleteMailing(DeleteView, PermissionRequiredMixin):
    """
    Класс удаления рассылки.
    """
    model = Mailing
    template_name = "mailings/delete_mailing_confirm.html"
    context_object_name = "mailing"


# ----------------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С ПОЛУЧАТЕЛЯМИ РАССЫЛКИ
# ----------------------------------------------------

class RecipientsList(ListView, PermissionRequiredMixin):
    """
    Класс отображения списка Получателей рассылки.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipient"


class AddRecipient(CreateView, PermissionRequiredMixin):
    """
    Класс добавления Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/add_recipient.html"
    context_object_name = "recipient"


class DetailRecipient(DetailView, PermissionRequiredMixin):
    """
    Класс просмотра детальной информации конкретного Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/detail_recipient.html"
    context_object_name = "recipient"


class UpdateRecipient(UpdateView, PermissionRequiredMixin):
    """
    Класс редактирования Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/update_recipient.html"
    context_object_name = "recipient"


class DeleteRecipient(DeleteView, PermissionRequiredMixin):
    """
    Класс удаления Получателя рассылки.
    """
    model = Recipient
    template_name = "mailing/delete_recipient_confirm.html"
    context_object_name = "recipient"


# ------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С СООБЩЕНИЯМИ
# ------------------------------------------

class MessageList(ListView, PermissionRequiredMixin):
    """
    Класс отображения списка сообщений.
    """
    model = Message
    template_name = "message/messages.html"
    context_object_name = "message"


class AddMessage(CreateView, PermissionRequiredMixin):
    """
    Класс добавления сообщений.
    """
    model = Message
    template_name = "message/add_message.html"
    context_object_name = "message"


class DetailMessage(DetailView, PermissionRequiredMixin):
    """
    Класс просмотра детальной информации конкретного сообщения.
    """
    model = Message
    template_name = "message/detail_message.html"
    context_object_name = "message"


class UpdateMessage(UpdateView, PermissionRequiredMixin):
    """
    Класс редактирования сообщения.
    """
    model = Message
    template_name = "message/update_message.html"
    context_object_name = "message"


class DeleteMessage(DeleteView, PermissionRequiredMixin):
    """
    Класс удаления сообщения.
    """
    model = Message
    template_name = "message/delete_message_confirm.html"
    context_object_name = "message"


# --------------
# БЛОК КОНТАКТОВ
# --------------
class Contacts(TemplateView):
    """
    Класс отображения страницы Контактов.
    """
    template_name = "mailing/contacts.html"
