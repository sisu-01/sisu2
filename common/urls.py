from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomAuthView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('config/', views.config, name='config'),
    path('config/profile', views.profile, name='profile'),
]
