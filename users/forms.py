from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('avatar', 'email', 'password1', 'password2', 'phone_number', 'country')


class UserEditProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('avatar', 'phone_number', 'country')
