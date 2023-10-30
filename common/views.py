from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import LoginForm, ProfileForm
from .models import Profile

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

@login_required(login_url='common:login')
def profile(request):
    try:
        profile = Profile.objects.get(id=1)
    except:
        profile = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'common/profile.html', context)