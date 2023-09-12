from django.contrib.auth import forms as auth_forms
from django import forms

class LoginForm(auth_forms.AuthenticationForm):
    remember = forms.BooleanField(required=False)