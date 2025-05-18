from django import forms

from .models import Mailing, Recipient, Message


class MailingNewForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipient")


class MailingUpdateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipient")


class RecipientNewForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "fullname", "comment",)


class RecipientUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "fullname", "comment",)


class MessageNewForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "message_body",)


class MessageUpdateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "message_body",)
