from django.urls import path

from .views.article import ArticlesView, IndexRedirect
from .views.login import Login
from .views.logout import Logout
from .views.publication import PublicationsView
from .views.detail import Detail
from .views.favorite import FavoriteView
from .views.register import Register
from .views.publish import Publish


urlpatterns = [
    path('', IndexRedirect.as_view(), name='index'),
    path('articles', ArticlesView.as_view(), name='articles'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(success_url="articles"), name='register'),
    path('publish', Publish.as_view(), name='publish'),
    path('publications', PublicationsView.as_view(), name='publications'),
    path('favorites', FavoriteView.as_view(), name='favorites'),
    path('detail/<int:pk>', Detail.as_view(), name='detail'),
]
