from django import forms
from .models import Reunion

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ['titre', 'date', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }