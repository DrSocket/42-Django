"""Root URL configuration for the d08 project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # The subject requires the default administration application to be kept.
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include("chat.urls")),
    # Bare / is not part of the subject; point it at the chat room list.
    path("", RedirectView.as_view(pattern_name="chat:rooms", permanent=False)),
]
