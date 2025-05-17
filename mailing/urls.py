from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingsTotalList, SearchResults, Contacts

app_name = MailingConfig.name

urlpatterns = [
    path("", MailingsTotalList.as_view(), name="mailing"),
    path("search-results/", SearchResults.as_view(), name="search_results"),
    path("contacts/", Contacts.as_view(), name="contacts"),
]
