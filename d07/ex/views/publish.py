from django.views.generic.edit import CreateView
from ..models import Article
from django.shortcuts import redirect


class Publish(CreateView):
    template_name = "ex/publish.html"
    model = Article
    fields = ['title', 'synopsis', 'content']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save() 

        return redirect('/')
    