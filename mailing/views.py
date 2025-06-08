import smtplib

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from config.settings import DEFAULT_FROM_EMAIL
from mailing.forms import MailingNewForm, MailingUpdateForm, RecipientNewForm, RecipientUpdateForm, MessageUpdateForm, \
    MessageNewForm
from mailing.models import Mailing, Message, Recipient, MailingAttempt


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
            status="Запущена").exists() else Mailing.objects.filter(status="Запущена").count()
        context[
            "unique_recipients"] = "данных нет" if not Recipient.objects.all().exists() else Recipient.objects.all().distinct().count()

        return context


class UserMailingsListAll(LoginRequiredMixin, ListView):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        qset = Mailing.objects.filter(owner=self.request.user)
        return qset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_mailings_total"] = Mailing.objects.filter(owner=self.request.user).count()
        context["user_mailings_started"] = Mailing.objects.filter(owner=self.request.user, status="Запущена").count()
        context["user_mailings_finished"] = Mailing.objects.filter(owner=self.request.user, status="Завершено").count()

        return context


class ManagerMailingsList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка всех рассылок, доступно только менеджерам.
    """
    model = Mailing
    template_name = "mailings/man_mailings.html"
    context_object_name = "mailings"
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["mailings_total"] = Mailing.objects.all().count()
        context["mailings_started"] = Mailing.objects.filter(status="Запущена").count()
        context["mailings_finished"] = Mailing.objects.filter(status="Завершена").count()

        return context


class UserMailingsListActive(LoginRequiredMixin, ListView):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        qset = Mailing.objects.filter(is_active=True, owner=self.request.user)
        return qset


class UserMailingsListNonActive(LoginRequiredMixin, ListView):
    """
    Класс отображения списка рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        qset = Mailing.objects.filter(is_active=False, owner=self.request.user)
        return qset


class AddMailing(LoginRequiredMixin, CreateView):
    """
    Класс добавления рассылки.
    """
    model = Mailing
    template_name = "mailings/add_mailing.html"
    form_class = MailingNewForm
    success_url = reverse_lazy("mailing:user_mailings")
    login_url = reverse_lazy("users:login")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['recipient'].queryset = form.fields['recipient'].queryset.filter(
            owner=self.request.user
        )
        form.fields['message'].queryset = form.fields['message'].queryset.filter(
            owner=self.request.user
        )
        return form

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.status = "Создана"

            self.object.save()
            form.save_m2m()

        return super().form_valid(form)


class SendMailingView(DetailView):
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.status = "Запущена"
        self.object.sent_at = timezone.now()

        subject = self.object.message.subject
        message = self.object.message.message_body
        from_email = DEFAULT_FROM_EMAIL

        recipient_emails = list(self.object.recipient.all().values_list('email', flat=True))
        self.execute_mailing(subject, message, from_email, recipient_emails)
        self.object.is_active = True

        self.object.save()
        return self.object

    def execute_mailing(self, subject, message, from_email, recipient_emails):
        for email in recipient_emails:
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [email],
                    fail_silently=False
                )
                print(f'Рассылка успешно отправлена адресату: {email}')
                MailingAttempt.objects.create(
                    attempt_date=timezone.now(),
                    attempt_status="Успешно",
                    mail_server_response="ok",
                    mailing=self.object
                )
            except smtplib.SMTPException as e:
                print(f'Ошибка отправки: {e}')
                MailingAttempt.objects.create(
                    attempt_date=timezone.now(),
                    attempt_status="Не успешно",
                    mail_server_response=str(e),
                    mailing=self.object
                )
        self.object.finished_at = timezone.now()
        self.object.save()


class DetailMailing(LoginRequiredMixin, DetailView):
    """
    Класс просмотра детальной информации конкретной рассылки.
    """
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')


class UpdateMailing(LoginRequiredMixin, UpdateView):
    """
    Класс редактирования рассылки.
    """
    model = Mailing
    template_name = "mailings/update_mailing.html"
    context_object_name = "mailing"
    form_class = MailingUpdateForm
    success_url = reverse_lazy('mailing:user_mailings')


class DeleteMailing(LoginRequiredMixin, DeleteView):
    """
    Класс удаления рассылки.
    """
    model = Mailing
    template_name = "mailings/delete_mailing_confirm.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')


# ----------------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С ПОПЫТКАМИ РАССЫЛОК
# ----------------------------------------------------

class UserAttemptsMailings(LoginRequiredMixin, ListView):
    """
    Класс отображения попыток рассылок.
    """
    model = MailingAttempt
    template_name = "attempts/attempts.html"
    context_object_name = "attempts"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        qset = MailingAttempt.objects.filter(owner_id=self.request.user.id)
        return qset


class DeleteAttempt(LoginRequiredMixin, DeleteView):
    """
    Класс удаления попытки рассылки.
    """
    model = MailingAttempt
    template_name = "attempts/delete_attempt_confirm.html"
    context_object_name = "attempt"
    success_url = reverse_lazy('mailing:attempts')


# ----------------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С ПОЛУЧАТЕЛЯМИ РАССЫЛКИ
# ----------------------------------------------------

class UserRecipientsList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка Получателей рассылки.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipients"

    def get_queryset(self):
        qset = Recipient.objects.filter(owner=self.request.user)
        return qset


class ManagerRecipientsList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка Получателей рассылки для менеджеров.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipients"

    def get_queryset(self):
        qset = Recipient.objects.all()
        return qset


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


class DeleteRecipient(LoginRequiredMixin, DeleteView):
    """
    Класс удаления Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/delete_recipient_confirm.html"
    context_object_name = "recipient"
    success_url = reverse_lazy('mailing:recipients')


# ------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С СООБЩЕНИЯМИ
# ------------------------------------------

class UserMessageList(LoginRequiredMixin, ListView):
    """
    Класс отображения списка сообщений.
    """
    model = Message
    template_name = "messages/messages.html"
    context_object_name = "messages"

    def get_queryset(self):
        qset = Message.objects.filter(owner=self.request.user)
        return qset


class AddMessage(LoginRequiredMixin, CreateView):
    """
    Класс добавления сообщений.
    """
    model = Message
    template_name = "messages/add_message.html"
    context_object_name = "message"
    form_class = MessageNewForm
    success_url = reverse_lazy('mailing:messages')

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


class DeleteMessage(LoginRequiredMixin, DeleteView):
    """
    Класс удаления сообщения.
    """
    model = Message
    template_name = "messages/delete_message_confirm.html"
    context_object_name = "message"
    success_url = reverse_lazy('mailing:messages')


# --------------
# БЛОК КОНТАКТОВ
# --------------
class Contacts(TemplateView):
    """
    Класс отображения страницы Контактов.
    """
    template_name = "mailings/contacts.html"
