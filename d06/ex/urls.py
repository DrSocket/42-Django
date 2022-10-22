from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('tip_like/<str:tip_id>', views.like, name='tip_like'),
    path('tip_dislike/<str:tip_id>', views.dislike, name='tip_dislike'),
    path('tip_del/<str:tip_id>', views.del_view, name='tip_del'),
]
