from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('post/<int:id>', views.post, name='post'),
    path('create/', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('upload/', staff_member_required(views.upload), name='upload'),
]
#r"^upload/" 이러는 이ㅠ가 있나?