# from django.views.generic import ListView
# from django.views.generic.base import RedirectView
# from ex.models import UserFavoriteArticle, Article

# class FavoriteView(ListView):
#     model = UserFavoriteArticle
#     template_name: str = "ex/favorites.html"

#     def get_queryset(self):
#         gs = Article.objects.filter(favorites__contains=self.request.user)

from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.db import DatabaseError
from django.shortcuts import redirect
from django.views.generic.list import ListView
from ex.models import Article, UserFavoriteArticle
from django.contrib.auth.mixins import LoginRequiredMixin
from ex.forms.favorite import FavoriteForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy


class FavoriteView(LoginRequiredMixin, ListView, FormView):
    template_name = "ex/favorites.html"
    form_class = FavoriteForm
    success_url = 'favorites'
    login_url = '/'
    model: UserFavoriteArticle = UserFavoriteArticle

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form: AuthenticationForm):
        article_id = form.cleaned_data['article']
        try:
            UserFavoriteArticle.objects.get(
                article=article_id, user=self.request.user).delete()
            messages.success(
                self.request, "Successful remove from favorites.")
        except UserFavoriteArticle.DoesNotExist as e:
            try:
                UserFavoriteArticle.objects.create(
                    user=self.request.user,
                    article=Article.objects.get(id=article_id),
                )
                messages.success(
                    self.request, "Successful add to favorites.")
            except DatabaseError as e:
                messages.error(
                    self.request, "Unsuccessful Add to favorite. Database error.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print (form)
        messages.error(
            self.request, "Unsuccessful Add to favorite. Invalid information.")
        return redirect('/')

    def get_form(self, form_class=None) -> BaseForm:
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(None, **self.get_form_kwargs())
