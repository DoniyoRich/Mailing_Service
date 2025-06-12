from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (AddMailing, AddMessage, AddRecipient, Contacts,
                           DeleteMailing, DeleteMessage, DeleteRecipient,
                           DetailMailing, DetailMessage, DetailRecipient,
                           MailingsTotalList, UserMessageList, UserRecipientsList,
                           UpdateMailing, UpdateMessage,
                           UpdateRecipient, SendMailingView, UserAttemptsMailings, DeleteAttempt,
                           UserMailingsListAll, UserMailingsListActive, UserMailingsListNonActive, ManagerMailingsList,
                           ManagerRecipientsList, ManagerBlockMailing, ManagerUnBlockMailing)

app_name = MailingConfig.name

urlpatterns = [
    # блок представлений для работы с рассылками...
    # ...на главной странице
    path("", MailingsTotalList.as_view(), name="mailing"),
    # ...на личной странице пользователя
    path("user-mailings/", UserMailingsListAll.as_view(), name="user_mailings"),
    path("user-mailings-active/", UserMailingsListActive.as_view(), name="user_mailings_active"),
    path("user-mailings-nonactive/", UserMailingsListNonActive.as_view(), name="user_mailings_nonactive"),
    path("add-mailing/", AddMailing.as_view(), name="add_mailing"),
    path("detail-mailing/<int:pk>/", DetailMailing.as_view(), name="detail_mailing"),
    path("update-mailing/<int:pk>/", UpdateMailing.as_view(), name="update_mailing"),
    path("delete-mailing/<int:pk>/", DeleteMailing.as_view(), name="delete_mailing"),
    path("send-mailing/<int:pk>/", SendMailingView.as_view(), name="send_mailing"),

    # блок представлений для работы с попытками
    path("attempts/", UserAttemptsMailings.as_view(), name="attempts"),
    path("delete-attempt/<int:pk>/", DeleteAttempt.as_view(), name="delete_attempt"),

    # блок представлений для работы с получателями рассылок
    path("recipients/", UserRecipientsList.as_view(), name="recipients"),
    path("add-recipient/", AddRecipient.as_view(), name="add_recipient"),
    path("detail-recipient/<int:pk>/", DetailRecipient.as_view(), name="detail_recipient"),
    path("update-recipient/<int:pk>/", UpdateRecipient.as_view(), name="update_recipient"),
    path("delete-recipient/<int:pk>/", DeleteRecipient.as_view(), name="delete_recipient"),

    # блок представлений для работы с сообщениями
    path("messages/", UserMessageList.as_view(), name="messages"),
    path("add-message/", AddMessage.as_view(), name="add_message"),
    path("detail-message/<int:pk>/", DetailMessage.as_view(), name="detail_message"),
    path("update-message/<int:pk>/", UpdateMessage.as_view(), name="update_message"),
    path("delete-message/<int:pk>/", DeleteMessage.as_view(), name="delete_message"),

    # блок представлений для менеджеров
    path("manager-mailings/", ManagerMailingsList.as_view(), name="man_mailings"),
    path("manager-recipients/", ManagerRecipientsList.as_view(), name="manager_recipients"),
    path("block-mailing/<int:pk>/", ManagerBlockMailing.as_view(), name="manager_block_mailing"),
    path("unblock-mailing/<int:pk>/", ManagerUnBlockMailing.as_view(), name="manager_unblock_mailing"),

    # блок представлений для работы с контактами
    path("contacts/", Contacts.as_view(), name="contacts"),
]
