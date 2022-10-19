from django.urls import path
from .views import init, populate, display

urlpatterns = [
    path("init/", init, name="ex02-init"),
    path('populate/', populate, name='ex02-populate'),
    path('display/', display, name='ex02-display'),
]