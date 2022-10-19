from django.urls import path
from .views import ex00View

urlpatterns = [
    path("init/", ex00View, name="postgres"),
]