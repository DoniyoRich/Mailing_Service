from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (AddMailing, AddMessage, AddRecipient, Contacts,
                           DeleteMailing, DeleteMessage, DeleteRecipient,
                           DetailMailing, DetailMessage, DetailRecipient,
                           MailingsTotalList, MessageList, RecipientsList,
                           SearchResults, UpdateMailing, UpdateMessage,
                           UpdateRecipient, UserMailingsList, SendMailingView)

app_name = MailingConfig.name

urlpatterns = [
    # блок представлений для работы с рассылками...
    # ...на главной странице
    path("", MailingsTotalList.as_view(), name="mailing"),
    path("search-results/", SearchResults.as_view(), name="search_results"),
    # ...на личной странице пользователя
    path("user-mailings/", UserMailingsList.as_view(), name="user_mailings"),
    path("add-mailing/", AddMailing.as_view(), name="add_mailing"),
    path("detail-mailing/<int:pk>/", DetailMailing.as_view(), name="detail_mailing"),
    path("update-mailing/<int:pk>/", UpdateMailing.as_view(), name="update_mailing"),
    path("delete-mailing/<int:pk>/", DeleteMailing.as_view(), name="delete_mailing"),
    path("send-mailing/<int:pk>/", SendMailingView.as_view(), name="send_mailing"),

    # блок представлений для работы с получателями рассылок
    path("recipients/", RecipientsList.as_view(), name="recipients"),
    path("add-recipient/", AddRecipient.as_view(), name="add_recipient"),
    path("detail-recipient/<int:pk>/", DetailRecipient.as_view(), name="detail_recipient"),
    path("update-recipient/<int:pk>/", UpdateRecipient.as_view(), name="update_recipient"),
    path("delete-recipient/<int:pk>/", DeleteRecipient.as_view(), name="delete_recipient"),

    # блок представлений для работы с сообщениями
    path("messages/", MessageList.as_view(), name="messages"),
    path("add-message/", AddMessage.as_view(), name="add_message"),
    path("detail-message/<int:pk>/", DetailMessage.as_view(), name="detail_message"),
    path("update-message/<int:pk>/", UpdateMessage.as_view(), name="update_message"),
    path("delete-message/<int:pk>/", DeleteMessage.as_view(), name="delete_message"),

    # блок представлений для работы с контактами
    path("contacts/", Contacts.as_view(), name="contacts"),
]
