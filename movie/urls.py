from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('insert', views.insert, name='insert'),
    path('select', views.select, name='select'),
]
