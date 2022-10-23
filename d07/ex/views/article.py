from django.views.generic import ListView
from django.views.generic.base import RedirectView
from ex.models import Article, UserFavoriteArticle
from typing import Any, Dict
from django.utils import timezone

class IndexRedirect(RedirectView):
    url = "articles"

class ArticlesView(ListView):
    template_name = 'ex/articles.html'
    model = Article
    queryset = Article.objects.filter().order_by('-created')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

