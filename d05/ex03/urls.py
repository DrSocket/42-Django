from django.urls import path
from .views import init, populate, display

urlpatterns = [
    path("init/", init, name="ex04-init"),
    path('populate/', populate, name='ex04-populate'),
    path('display/', display, name='ex04-display'),
]