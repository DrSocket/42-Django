from typing import Any
from django import http
from django.http.response import HttpResponseBase
from ex.forms.favorite import FavoriteForm
from ex.models import Article
from django.views.generic import DetailView

class Detail(DetailView):
    model = Article
    template_name = 'ex/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['object']
        context["favoriteForm"] = FavoriteForm(article.id)
        return context