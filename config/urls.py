from django.contrib import admin
from django.template.context_processors import static
from django.urls import path

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
