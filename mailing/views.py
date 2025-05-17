from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import MailingNewForm, MailingUpdateForm
from mailing.models import Mailing, Message, Recipient


# -----------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С РАССЫЛКАМИ
# -----------------------------------------

class MailingsTotalList(ListView):
    """
    Класс отображения списка всех рассылок в системе.
    """
    model = Mailing
    template_name = "mailings/mailings.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total"] = Mailing.objects.all().count()
        context["total_active"] = "данных нет" if not Mailing.objects.filter(
            status="Запущена").exists() else Mailing.objects.filter(status="Запущена")
        context[
            "unique_recipients"] = "данных нет" if not Recipient.objects.all().exists() else Recipient.objects.all().distinct()

        return context


class SearchResults(ListView):
    """
    Класс отображения результатов поиска рассылок.
    """
    model = Mailing
    template_name = "mailings/search_results.html"
    context_object_name = "search_results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_found"] = "20"
        context["total_active"] = 10

        return context


class UserMailingsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    permission_required = "view_mailing"
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "u_mailings"


class AddMailing(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс добавления рассылки.
    """
    permission_required = "can_add_mailing"
    model = Mailing
    template_name = "mailings/add_mailing.html"
    context_object_name = "mailing"
    form_class = MailingNewForm
    success_url = reverse_lazy('mailing:mailing')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class DetailMailing(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Класс просмотра детальной информации конкретной рассылки.
    """
    permission_required = "view_mailing"
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"


class UpdateMailing(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс редактирования рассылки.
    """
    permission_required = "change_mailing"
    model = Mailing
    template_name = "mailings/update_mailing.html"
    context_object_name = "mailing"
    form_class = MailingUpdateForm
    success_url = reverse_lazy('mailing:mailing')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class DeleteMailing(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс удаления рассылки.
    """
    permission_required = "delete_mailing"
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
    context_object_name = "recipients"


class DetailRecipient(DetailView, PermissionRequiredMixin):
    """
    Класс просмотра детальной информации конкретного Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/detail_recipient.html"
    context_object_name = "recipient"


class AddRecipient(CreateView, PermissionRequiredMixin):
    """
    Класс добавления Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/add_recipient.html"
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
    context_object_name = "messages"


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
    template_name = "mailings/contacts.html"
