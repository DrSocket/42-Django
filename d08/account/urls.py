from django.urls import path

from .views import login_view, Logout, login_ajax, logout_ajax


urlpatterns = [
    path('account/', login_view, name='account'),
    path('login/', login_ajax, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('logout_ajax/', logout_ajax, name='logout_ajax'),

]
