from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from ex.forms.login import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

class Login(LoginView):
    template_name = "ex/login.html"
    next_page = 'ex/articles.html'
    # form_class = LoginForm

    # def form_valid(self, form: LoginForm):
    #     username = form.cleaned_data.get('username')
    #     print(f'hello {username}')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(self.request, username=username, password=password)
    #     if user is None or user is 0:
    #         messages.error(self.request, "Invalid username or password.")
    #         return
    #     login(self.request, user)
    #     messages.info(self.request, f"You are now logged in as {username}.")
    #     return super().form_valid(form)

    # def form_invalid(self, form):
    #     return super().form_invalid(form)