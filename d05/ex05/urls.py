from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.Init.as_view(), name='ex05-init'),
    path('populate/', views.Populate.as_view(), name='ex05-populate'),
    path('display/', views.Display.as_view(), name='ex05-display'),
    path('remove/', views.Remove.as_view(), name='ex05-remove'),
]
