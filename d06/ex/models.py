from django.db import models
from django.contrib.auth.models import User

class TipDay(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_tips", blank=True,)
    dislikes = models.ManyToManyField(User, related_name="disliked_tips", blank=True,)

    class Meta:
        ordering = ['-date']
