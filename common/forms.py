from django.contrib.auth import forms as auth_forms
from django import forms
from .models import Profile

class LoginForm(auth_forms.AuthenticationForm):
    remember = forms.BooleanField(required=False)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname','desc','image']