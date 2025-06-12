from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('avatar', 'email', 'password1', 'password2', 'phone_number', 'country')


class UserEditProfileForm(UserChangeForm):
    """
    Форма редактирования профиля пользователя.
    """

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('avatar', 'phone_number', 'country')


class UserBlockProfileForm(UserChangeForm):
    """
    Форма блокировки пользователя.
    """

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('is_active',)
