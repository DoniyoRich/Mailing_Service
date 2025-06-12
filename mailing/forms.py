from django import forms

from .models import Mailing, Recipient, Message


class MailingNewForm(forms.ModelForm):
    """
    Форма для новой рассылки.
    """

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
    """
    Форма редактирования рассылки.
    """

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
    """
    Форма для нового получателя рассылки.
    """

    class Meta:
        model = Recipient
        fields = ("email", "fullname", "comment",)


class RecipientUpdateForm(forms.ModelForm):
    """
    Форма редактирования получателя рассылки.
    """

    class Meta:
        model = Recipient
        fields = ("email", "fullname", "comment",)


class MessageNewForm(forms.ModelForm):
    """
    Форма для нового сообщения.
    """

    class Meta:
        model = Message
        fields = ("subject", "message_body",)


class MessageUpdateForm(forms.ModelForm):
    """
    Форма редактирования нового сообщения.
    """

    class Meta:
        model = Message
        fields = ("subject", "message_body",)


class MailingBlockForm(forms.ModelForm):
    """
    Форма отключения рассылки.
    """

    class Meta:
        model = Mailing
        fields = ('is_active',)
