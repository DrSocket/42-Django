from django import forms
from .models import TipDay

class MsgForm(forms.Form):
    # text_field = forms.TextInput(label='msg',)
    msg = forms.CharField(label='Message', max_length=128)

class UserLogin(forms.Form):
    username = forms.CharField(label='username', max_length=128)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput)

class TipForm(forms.ModelForm):
    class Meta:
        model = TipDay
        fields = ['content']
