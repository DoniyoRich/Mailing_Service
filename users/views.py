from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from users.forms import UserRegisterForm, UserEditProfileForm
from users.models import CustomUser


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/reg_user_form.html'
    success_url = reverse_lazy('mailing:user_mailings')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

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


class UsersListView(ListView):
    model = CustomUser
    template_name = "users/users.html"
    context_object_name = "users"


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "users/user_profile_detail.html"


class UserEditProfileView(UpdateView):
    model = CustomUser
    form_class = UserEditProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy('mailing:user_mailings')


class UserDeleteProfileView(DeleteView):
    model = CustomUser
    template_name = "users/delete_profile.html"
