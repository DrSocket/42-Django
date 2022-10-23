from django import forms
from django.forms.widgets import HiddenInput


class FavoriteForm(forms.Form):
    article = forms.IntegerField(widget=HiddenInput(), required=True)

    def __init__(self, article, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.article = article

        if article is not None:
            self.fields['article'].initial = article

