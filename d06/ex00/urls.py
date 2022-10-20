from django.urls import path
from . import views

urlpatterns = [
    path('/', views.Ex00.as_view(), name='ex00'),
]
