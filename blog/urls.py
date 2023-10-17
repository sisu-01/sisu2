from django.contrib.admin.views.decorators import staff_member_required
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
    path('upload_image/', staff_member_required(views.ckeditor_upload_image), name='upload_image'),
    
    path('tree/', staff_member_required(views.tree), name='set_tree'),
    path('get_tree/', staff_member_required(views.get_tree), name='get_tree'),
    path('select_tree/', staff_member_required(views.select_tree), name='select_tree'),
    path('create_tree/', staff_member_required(views.save_tree), name='save_tree'),
    path('delete_tree/', staff_member_required(views.delete_tree), name='delete_tree'),
]
#//수정 login_required는 로그인 사용자 모두
#//수정 staff_membe_required는 스태프만. 이거 구분해서 정해라
#//수정 r"^upload/" 이러는 이ㅠ가 있나?