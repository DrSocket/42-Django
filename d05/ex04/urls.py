from django.urls import path
from .views import Init, Populate, Display, Remove

urlpatterns = [
    path('init/', Init.as_view(), name='ex04-init'),
    path('populate/', Populate.as_view(), name='ex04-populate'),
    path('display/', Display.as_view(), name='ex04-display'),
    path('remove/', Remove.as_view(), name='ex04-remove'),
]
