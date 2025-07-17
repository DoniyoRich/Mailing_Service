from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import EmailMessage, get_connection
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from config.settings import DEFAULT_FROM_EMAIL
from mailing.forms import (MailingBlockForm, MailingNewForm, MailingUpdateForm,
                           MessageNewForm, MessageUpdateForm, RecipientNewForm,
                           RecipientUpdateForm)
from mailing.models import Mailing, MailingAttempt, Message, Recipient


# -----------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С РАССЫЛКАМИ
# -----------------------------------------


class MailingsTotalList(ListView):
    """
    Представление отображения информации по рассылкам на главной странице.
    """
    model = Mailing
    template_name = "mailings/mailings.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total"] = Mailing.objects.all().count()
        context["total_active"] = "данных нет" if not Mailing.objects.filter(
            status="Завершена").exists() else Mailing.objects.filter(status="Завершена").count()
        context["total_failed"] = "данных нет" if not Mailing.objects.filter(
            status="Ошибка").exists() else Mailing.objects.filter(status="Ошибка").count()
        context[
            "unique_recipients"] = "данных нет" \
            if not Recipient.objects.all().exists() else Recipient.objects.all().distinct().count()

        return context


class UserMailingsListAll(LoginRequiredMixin, ListView):
    """
    Представление отображения списка рассылок определенного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = Mailing.objects.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_mailings_total"] = Mailing.objects.filter(owner=self.request.user).count()
        context["user_mailings_started"] = Mailing.objects.filter(owner=self.request.user, status="Запущена").count()
        context["user_mailings_finished"] = Mailing.objects.filter(owner=self.request.user, status="Завершена").count()

        return context


class ManagerMailingsList(LoginRequiredMixin, ListView):
    """
    Представление отображения списка всех рассылок, доступно только менеджерам.
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class UserMailingsListActive(LoginRequiredMixin, ListView):
    """
    Представление отображения списка активных рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = Mailing.objects.filter(is_active=True, owner=self.request.user)
        return queryset


class UserMailingsListNonActive(LoginRequiredMixin, ListView):
    """
    Представление отображения списка неактивных рассылок конкретного Пользователя.
    """
    model = Mailing
    template_name = "mailings/user_mailings.html"
    context_object_name = "user_mailings"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = Mailing.objects.filter(is_active=False, owner=self.request.user)
        return queryset


class AddMailing(LoginRequiredMixin, CreateView):
    """
    Представление добавления рассылки.
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
    """
    Представление отправки рассылки получателям.
    """
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        """
        Функция формирует исходные данные для функции отправки сообщения получателям,
        а также устанавливает статус рассылки.
        """
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
        """
        Функция отправки e-mail сообщения.
        """
        connection = None
        try:
            connection = get_connection(
                fail_silently=False,
            )
            connection.open()

            for email in recipient_emails:
                attempt = MailingAttempt(
                    attempt_date=timezone.now(),
                    mailing=self.object,
                    owner=self.request.user,
                    recipient_email=email
                )

                try:
                    email_msg = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email=from_email,
                        to=[email],
                        connection=connection,
                        headers={
                            'Return-Path': DEFAULT_FROM_EMAIL,
                            'X-Mailer': 'Django Mailing System'
                        }
                    )

                    sent_count = email_msg.send()

                    if sent_count == 0:
                        raise SMTPException("Сервер не принял письмо")

                    attempt.attempt_status = "Успешно"
                    attempt.mail_server_response = "Принято сервером"

                except SMTPException as e:
                    error_msg = str(e)
                    print(f'Ошибка отправки на {email}: {error_msg}')
                    attempt.attempt_status = "Не успешно"
                    attempt.mail_server_response = error_msg[:255]

                except Exception as e:
                    error_msg = f"Неожиданная ошибка: {str(e)}"
                    print(error_msg)
                    attempt.attempt_status = "Не успешно"
                    attempt.mail_server_response = error_msg[:255]

                finally:
                    attempt.save()

        finally:
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

        self.object.finished_at = timezone.now()

        if MailingAttempt.objects.filter(mailing=self.object, attempt_status="Успешно").exists():
            self.object.status = "Завершена"
        else:
            self.object.status = "Ошибка"
        self.object.save()


class DetailMailing(LoginRequiredMixin, DetailView):
    """
    Представление просмотра детальной информации по определенной рассылке.
    """
    model = Mailing
    template_name = "mailings/detail_mailing.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = cache.get("detail_mailing")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("detail_mailing", queryset, 60 * 1)  # Кешируем данные на минуту
        return queryset


class UpdateMailing(LoginRequiredMixin, UpdateView):
    """
    Представление редактирования рассылки.
    """
    model = Mailing
    template_name = "mailings/update_mailing.html"
    context_object_name = "mailing"
    form_class = MailingUpdateForm
    success_url = reverse_lazy('mailing:user_mailings')


class DeleteMailing(LoginRequiredMixin, DeleteView):
    """
    Представление удаления рассылки.
    """
    model = Mailing
    template_name = "mailings/delete_mailing_confirm.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mailing:user_mailings')
    login_url = reverse_lazy('users:login')


class ManagerBlockMailing(LoginRequiredMixin, UpdateView):
    """
    Представление отключения рассылки менеджером.
    """
    model = Mailing
    form_class = MailingBlockForm
    template_name = "mailings/block_mailing.html"
    success_url = reverse_lazy('mailing:man_mailings')


class ManagerUnBlockMailing(LoginRequiredMixin, UpdateView):
    """
    Представление включения рассылки менеджером.
    """
    model = Mailing
    form_class = MailingBlockForm
    template_name = "mailings/unblock_mailing.html"
    success_url = reverse_lazy('mailing:man_mailings')


# ----------------------------------------------------
# БЛОК ПРЕДСТАВЛЕНИЙ ПО РАБОТЕ С ПОПЫТКАМИ РАССЫЛОК
# ----------------------------------------------------

class UserAttemptsMailings(LoginRequiredMixin, ListView):
    """
    Представление отображения попыток рассылок.
    """
    model = MailingAttempt
    template_name = "attempts/attempts.html"
    context_object_name = "attempts"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = MailingAttempt.objects.filter(owner_id=self.request.user.id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['att_total'] = MailingAttempt.objects.filter(owner_id=self.request.user.id).count()
        context['att_success'] = MailingAttempt.objects.filter(owner_id=self.request.user.id,
                                                               attempt_status="Успешно").count()
        context['att_fail'] = MailingAttempt.objects.filter(owner_id=self.request.user.id,
                                                            attempt_status="Не успешно").count()
        return context


class DeleteAttempt(LoginRequiredMixin, DeleteView):
    """
    Представление удаления попытки рассылки.
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
    Представление отображения списка Получателей рассылки.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipients"

    def get_queryset(self):
        queryset = Recipient.objects.filter(owner=self.request.user)
        return queryset


class ManagerRecipientsList(LoginRequiredMixin, ListView):
    """
    Представление отображения списка Получателей рассылки для менеджеров.
    """
    model = Recipient
    template_name = "recipients/recipients.html"
    context_object_name = "recipients"

    def get_queryset(self):
        queryset = Recipient.objects.all()
        return queryset


class DetailRecipient(LoginRequiredMixin, DetailView):
    """
    Представление просмотра детальной информации конкретного Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/detail_recipient.html"
    context_object_name = "recipient"

    def get_queryset(self):
        queryset = cache.get("recipient")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("recipient", queryset, 60 * 1)  # Кешируем данные на минуту
        return queryset


class AddRecipient(LoginRequiredMixin, CreateView):
    """
    Представление добавления Получателя рассылки.
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
    Представление редактирования Получателя рассылки.
    """
    model = Recipient
    template_name = "recipients/update_recipient.html"
    context_object_name = "recipient"
    form_class = RecipientUpdateForm
    success_url = reverse_lazy('mailing:recipients')


class DeleteRecipient(LoginRequiredMixin, DeleteView):
    """
    Представление удаления Получателя рассылки.
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
    Представление отображения списка сообщений.
    """
    model = Message
    template_name = "messages/messages.html"
    context_object_name = "messages"

    def get_queryset(self):
        queryset = Message.objects.filter(owner=self.request.user)
        return queryset


class AddMessage(LoginRequiredMixin, CreateView):
    """
    Представление добавления сообщения.
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
    Представление просмотра детальной информации конкретного сообщения.
    """
    model = Message
    template_name = "messages/detail_message.html"
    context_object_name = "message"

    def get_queryset(self):
        queryset = cache.get("message")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("message", queryset, 60 * 1)  # Кешируем данные на минуту
        return queryset


class UpdateMessage(LoginRequiredMixin, UpdateView):
    """
    Представление редактирования сообщения.
    """
    model = Message
    template_name = "messages/update_message.html"
    context_object_name = "message"
    form_class = MessageUpdateForm
    success_url = reverse_lazy('mailing:messages')


class DeleteMessage(LoginRequiredMixin, DeleteView):
    """
    Представление удаления сообщения.
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
    Представление отображения страницы Контактов.
    """
    template_name = "mailings/contacts.html"
