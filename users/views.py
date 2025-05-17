from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm


class UserRegisterView(CreateView, Permission):
    form_class = UserRegisterForm
    template_name = 'users/reg_user_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        can_edit_product = Permission.objects.get(codename="change_product")
        can_delete_product = Permission.objects.get(codename="delete_product")
        user.user_permissions.add(can_edit_product, can_delete_product)

        # СТРОКА НИЖЕ РАБОТОСПОСОБНАЯ, ПРОСТО ВРЕМЕННО ОТКЛЮЧЕНА
        # self.send_welcome_email(user.email)

        return super().form_valid(form)

# ФУНКЦИЯ НИЖЕ РАБОТОСПОСОБНА, ОНА ВРЕМЕННО ОТКЛЮЧЕНА ДЛЯ ПРОВЕРКИ ДОМАШКИ
# НА ПРАВА ДОСТУПА, ТАК КАК ОТПРАВЛЯЕТ СООБЩЕНИЯ НА РЕАЛЬНЫЕ АДРЕСА
# ЭЛЕКТРОННОЙ ПОЧТЫ.
# ПРИ ТЕСТИРОВАНИИ ФУКЦИОНАЛА ПРАВ ДОСТУПА МОГУТ БЫТ СОЗДАНЫ РАЗНЫЕ
# НЕСУЩЕСТВУЮЩИЕ ПОЛЬЗОВАТЕЛИ, ЧТО ВЫЗОВЕТ ОШИБКУ

    # def send_welcome_email(self, user_email):
    #     subject = 'Добро пожаловать!'
    #     message = 'Спасибо, что зарегистрировались в нашем интернет-магазине!'
    #     from_email = EMAIL_HOST_USER
    #     recipient_list = [user_email]
    #     send_mail(subject, message, from_email, recipient_list)
