from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (CustomLoginView, UserBlockProfileView,
                         UserDeleteProfileView, UserEditProfileView,
                         UserProfileView, UserRegisterView, UsersListView,
                         UserUnBlockProfileView)

app_name = UsersConfig.name

urlpatterns = [
    # блок представлений для регистрации и авторизации пользователя,
    # просмотра и редактирования его профиля,
    # а также представления блокировки и разблокировки пользователя менеджером
    path("login/", CustomLoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("view-profile/<int:pk>/", UserProfileView.as_view(), name="view_profile"),
    path("edit-profile/<int:pk>/", UserEditProfileView.as_view(), name="edit_profile"),
    path("delete-profile/<int:pk>/", UserDeleteProfileView.as_view(), name="delete_profile"),
    path("block-profile/<int:pk>/", UserBlockProfileView.as_view(), name="block_profile"),
    path("unblock-profile/<int:pk>/", UserUnBlockProfileView.as_view(), name="unblock_profile"),
    path("users-list/", UsersListView.as_view(), name="users_list"),

    # блок представлений для восстановления пароля пользователя
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url='done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/users/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
