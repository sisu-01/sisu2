from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/<int:id>', views.listz, name='list'),
    path('post/<int:id>', views.post, name='post'),
    path('create/', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('upload/', staff_member_required(views.upload), name='upload'),
    
    path('tree/', staff_member_required(views.tree), name='tree'),
    path('get_tree/', staff_member_required(views.get_tree), name='get_tree'),
    path('tree_select/', staff_member_required(views.select_tree), name='tree_select'),
    path('tree_create/', staff_member_required(views.create_tree), name='tree_create'),
    path('tree_delete/', staff_member_required(views.delete_tree), name='tree_delete'),
]
#r"^upload/" 이러는 이ㅠ가 있나?