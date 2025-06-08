from django import forms

from .models import Mailing, Recipient, Message


class MailingNewForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipient")

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if self.user and 'recipient' in self.fields:
                self.fields['recipient'].queryset = self.fields['recipient'].queryset.filter(
                    owner=self.user
                )

            if self.user and 'message' in self.fields:
                self.fields['message'].queryset = self.fields['message'].queryset.filter(
                    owner=self.user
                )


class MailingUpdateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipient")

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if self.user and 'recipient' in self.fields:
                self.fields['recipient'].queryset = self.fields['recipient'].queryset.filter(
                    owner=self.user
                )


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
