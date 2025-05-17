from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'phone_number', 'avatar', 'country')
