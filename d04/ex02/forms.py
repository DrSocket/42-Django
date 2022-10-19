from django import forms


class History(forms.Form):
    u_input = forms.CharField(label='Type some text ')