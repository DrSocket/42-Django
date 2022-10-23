from django.contrib.auth.views import LogoutView

class Logout(LogoutView):
    next_page = 'ex:index'


