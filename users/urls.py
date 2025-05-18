from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, UserProfileView, UserEditProfileView, UserDeleteProfileView, UsersListView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("view-profile/<int:pk>/", UserProfileView.as_view(), name="view_profile"),
    path("edit-profile/<int:pk>/", UserEditProfileView.as_view(), name="edit_profile"),
    path("delete-profile/<int:pk>/", UserDeleteProfileView.as_view(), name="delete_profile"),

    path("users-list/", UsersListView.as_view(), name="users_list"),
]
