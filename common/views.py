from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .forms import LoginForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

class CustomAuthView(auth_views.LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if not remember:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super().form_valid(form)
    
def config(request):
    return render(request, 'common/config.html')

def profile(request):
    return render(request, 'common/profile.html')