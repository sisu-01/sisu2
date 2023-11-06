from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf import settings
from .forms import LoginForm, ProfileForm
from .models import Profile
from pathlib import Path
import os

# Create your views here.
def index(request):
    context = {
        'og': {
            'title': '첫 화면',
            'desc': '성장하는 사이트',
        }
    }
    return render(request, 'index.html', context)

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

@login_required(login_url='common:login')
def profile(request):
    try:
        profile = Profile.objects.get(id=1)
        old_image = str(profile.image)
    except:
        profile = None
        old_image = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            pf = form.save(commit=False)
            pf.save()
            if(old_image != None and old_image != str(pf.image)):
                if os.path.isfile(Path(settings.MEDIA_ROOT, old_image)):
                    os.remove(Path(settings.MEDIA_ROOT, old_image))
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'common/profile.html', context)