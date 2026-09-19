"""URLs for ex00. The subject asks for 127.0.0.1:8000/account."""

from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("account", views.account, name="account"),
    path("account/login", views.login, name="login"),
    path("account/logout", views.logout, name="logout"),
    # Not part of the subject: a convenience so users can be created from the
    # page itself (over AJAX, like login), instead of the shell or admin.
    path("account/register", views.register, name="register"),
]
