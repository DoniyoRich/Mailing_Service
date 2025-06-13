from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from mailing.constants import MANAGER_GROUP_NAME
from users.forms import (UserBlockProfileForm, UserEditProfileForm,
                         UserRegisterForm)
from users.models import CustomUser


class UserRegisterView(CreateView):
    """
    Представление регистрации пользователя.
    """
    form_class = UserRegisterForm
    template_name = 'users/reg_user_form.html'
    success_url = reverse_lazy('mailing:user_mailings')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class CustomLoginView(LoginView):
    """
    Представление авторизации пользователя.
    """
    template_name = 'users/login.html'

    redirect_authenticated_user = False

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name=MANAGER_GROUP_NAME).exists():
            return reverse_lazy('mailing:man_mailings')
        return reverse_lazy('mailing:user_mailings')


class UsersListView(ListView):
    """
    Представление вывода списка пользователей.
    """
    model = CustomUser
    template_name = "users/users.html"
    context_object_name = "users"


class UserProfileView(DetailView):
    """
    Представление просмотра профиля пользователя.
    """
    model = CustomUser
    template_name = "users/user_profile_detail.html"
    context_object_name = "custom_user"


class UserEditProfileView(UpdateView):
    """
    Представление редактирования профиля пользователя.
    """
    model = CustomUser
    form_class = UserEditProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy('users:users_list')
    context_object_name = "custom_user"


class UserBlockProfileView(UpdateView):
    """
    Представление блокировки пользователя.
    """
    model = CustomUser
    form_class = UserBlockProfileForm
    template_name = "users/block_profile.html"
    success_url = reverse_lazy('users:users_list')
    context_object_name = "custom_user"


class UserUnBlockProfileView(UpdateView):
    """
    Представление разблокировки профиля пользователя.
    """
    model = CustomUser
    form_class = UserBlockProfileForm
    template_name = "users/unblock_profile.html"
    success_url = reverse_lazy('users:users_list')
    context_object_name = "custom_user"


class UserDeleteProfileView(DeleteView):
    """
    Представление удаления профиля пользователя.
    """
    model = CustomUser
    template_name = "users/delete_profile.html"
    context_object_name = "custom_user"
