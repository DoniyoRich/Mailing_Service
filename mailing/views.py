import smtplib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import MailingNewForm, MailingUpdateForm, RecipientNewForm, RecipientUpdateForm, MessageUpdateForm, \
    MessageNewForm
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
            "unique_recipients"] = "данных нет" if not Recipient.objects.all().exists() else Recipient.objects.all().distinct().count()

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


class UserMailingsList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    # permission_required = "view_mailing"
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')


class AddMailing(LoginRequiredMixin, CreateView):
    """
    Класс добавления рассылки.
    """
    # permission_required = "can_add_mailing"
    model = Mailing
    template_name = "mailings/add_mailing.html"
    context_object_name = "mailing"
    form_class = MailingNewForm
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class SendMailingView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.status = ""
        subject = ""
        message = ""
        from_email = ""
        recipient_list = ""
        # self.execute_mailing(subject, message, from_email, recipient_list)
        self.object.save()
        return self.object

    def execute_mailing(self, subject, message, from_email, recipient_list):
        try:
            sent_count = send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )
            # sent_count = send_mail(
            #     'Важная новость',
            #     'Текст сообщения...',
            #     'noreply@company.com',
            #     ['user1@mail.com', 'user2@mail.com', 'user3@mail.com'],
            #     fail_silently=False
            # )
            print(f'Успешно отправлено писем: {sent_count}')
        except smtplib.SMTPException as e:
            print(f'Ошибка отправки: {e}')


class DetailMailing(LoginRequiredMixin, DetailView):
    """
    Класс просмотра детальной информации конкретной рассылки.
    """
    # permission_required = "view_mailing"
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')


class UpdateMailing(LoginRequiredMixin, UpdateView):
    """
    Класс редактирования рассылки.
    """
    # permission_required = "change_mailing"
    model = Mailing
    template_name = "mailings/update_mailing.html"
    context_object_name = "mailing"
    form_class = MailingUpdateForm
    success_url = reverse_lazy('mailing:user_mailings')
    # login_url = reverse_lazy('users:login')


class DeleteMailing(LoginRequiredMixin, DeleteView):
    """
    Класс удаления рассылки.
    """
    # permission_required = "delete_mailing"
    model = Mailing
    template_name = "mailings/delete_mailing_confirm.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    # login_url = reverse_lazy('users:login')


# ----------------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С ПОЛУЧАТЕЛЯМИ РАССЫЛКИ
# ----------------------------------------------------

class RecipientsList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка Получателей рассылки.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipients"


class DetailRecipient(LoginRequiredMixin, DetailView):
    """
    Класс просмотра детальной информации конкретного Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/detail_recipient.html"
    context_object_name = "recipient"


class AddRecipient(LoginRequiredMixin, CreateView):
    """
    Класс добавления Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/add_recipient.html"
    context_object_name = "recipient"
    form_class = RecipientNewForm
    success_url = reverse_lazy('mailing:recipients')

    # login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class UpdateRecipient(LoginRequiredMixin, UpdateView):
    """
    Класс редактирования Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/update_recipient.html"
    context_object_name = "recipient"
    form_class = RecipientUpdateForm
    success_url = reverse_lazy('mailing:recipients')
    # login_url = reverse_lazy('users:login')


class DeleteRecipient(LoginRequiredMixin, DeleteView):
    """
    Класс удаления Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/delete_recipient_confirm.html"
    context_object_name = "recipient"
    success_url = reverse_lazy('mailing:recipients')
    # login_url = reverse_lazy('users:login')


# ------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С СООБЩЕНИЯМИ
# ------------------------------------------

class MessageList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка сообщений.
    """
    model = Message
    template_name = "messages/messages.html"
    context_object_name = "messages"


class AddMessage(LoginRequiredMixin, CreateView):
    """
    Класс добавления сообщений.
    """
    model = Message
    template_name = "messages/add_message.html"
    context_object_name = "message"
    form_class = MessageNewForm
    success_url = reverse_lazy('mailing:messages')

    # login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class DetailMessage(LoginRequiredMixin, DetailView):
    """
    Класс просмотра детальной информации конкретного сообщения.
    """
    model = Message
    template_name = "messages/detail_message.html"
    context_object_name = "message"


class UpdateMessage(LoginRequiredMixin, UpdateView):
    """
    Класс редактирования сообщения.
    """
    model = Message
    template_name = "messages/update_message.html"
    context_object_name = "message"
    form_class = MessageUpdateForm
    success_url = reverse_lazy('mailing:messages')
    # login_url = reverse_lazy('users:login')


class DeleteMessage(LoginRequiredMixin, DeleteView):
    """
    Класс удаления сообщения.
    """
    model = Message
    template_name = "messages/delete_message_confirm.html"
    context_object_name = "message"
    success_url = reverse_lazy('mailing:messages')
    # login_url = reverse_lazy('users:login')


# --------------
# БЛОК КОНТАКТОВ
# --------------
class Contacts(TemplateView):
    """
    Класс отображения страницы Контактов.
    """
    template_name = "mailings/contacts.html"
