from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='index'),
    path('kobis', views.call_kobis_api, name='kobis'),
    path('save', views.save_movie, name='save'),
    path('get', views.get_movie, name='get'),
    path('delete', views.delete_movie, name='delete'),
]
