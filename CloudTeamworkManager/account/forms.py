from django.forms import ModelForm
from django import forms
from .models import UserProfile

class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(max_length=16, min_length=6)
    msgcode = forms.CharField(max_length=4, min_length=4)
    phone_number = forms.CharField(max_length=11, min_length=11)

class LoginForm(forms.Form):
    password = forms.CharField(max_length=16, min_length=6)
    user_name = forms.CharField(max_length=20, min_length=6)