from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib import messages


class Register(FormView):
    template_name = "ex/register.html"
    form_class = UserCreationForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logined!')
            return redirect('/')
        return super().get(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful registration. Invalid information.")
        return super().form_invalid(form)
