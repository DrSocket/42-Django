from django.urls import path
from .views import ex00View

urlpatterns = [
    path("", ex00View, name="markdown"),
]