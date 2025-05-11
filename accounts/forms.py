from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AdminUser

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = AdminUser
        fields = ['email', 'full_name', 'password']

class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
