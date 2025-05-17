from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing


class MailingNewForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipient")


"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in BANNED_WORDS:
            if word.lower() in name:
                raise ValidationError(f'Поле содержит запрещенное слово - "{word}", просьба исправить на другое')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in BANNED_WORDS:
            if word.lower() in description:
                raise ValidationError(f'Поле содержит запрещенное слово - "{word}", просьба исправить на другое')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price
"""


class MailingUpdateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('__all__')
