from django.urls import path
from .views import homePageView

urlpatterns = [
    path("helloworld", homePageView, name="home"),
]