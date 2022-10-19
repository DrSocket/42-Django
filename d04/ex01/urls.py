from django.urls import path
from .views import django, display, templates

urlpatterns = [
    path("django", django, name="django"),
    path("display", display, name="display"),
    path("templates", templates, name="templates"),
]