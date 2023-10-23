from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post_list/<str:id>', views.get_post_list, name='post_list'),
    path('post/<int:id>', views.get_post, name='get_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:id>', views.update_post, name='update_post'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('upload_image/', views.ckeditor_upload_image, name='upload_image'),

    path('get_cmt/', views.get_cmt, name='get_cmt'),
    path('create_cmt/', views.create_cmt, name='create_cmt'),
    path('delete_cmt/', views.delete_cmt, name='delete_cmt'),

    path('tree/', views.tree, name='set_tree'),
    path('get_tree/', views.get_tree, name='get_tree'),
    path('select_tree/', views.select_tree, name='select_tree'),
    path('create_tree/', views.save_tree, name='save_tree'),
    path('delete_tree/', views.delete_tree, name='delete_tree'),
]
#//수정 login_required는 로그인 사용자 모두