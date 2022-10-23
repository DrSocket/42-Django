from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    synopsis = models.CharField(max_length=312, null=False)
    content = models.TextField(null=False)

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ['-created']

class UserFavoriteArticle(models.Model):
    user = models.ForeignKey(User, verbose_name=(
        "UserFavoriteArticle user"), on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(Article, verbose_name=(
        "UserFavoriteArticle article"), on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return str(self.article.title)