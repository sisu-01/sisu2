from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Menu, Post
from .forms import PostForm

# Create your views here.
def index(request):
    temp = Menu.objects.all().order_by('seq')
    result = get_menu_tree(temp)
    context = {
        'menus': result
    }
    return render(request, 'blog/blog.html', context)

def get_menu_tree(menus, parent=None):
    tree = []
    for menu in menus:
        if menu.id_parent_id == parent:
            child = get_menu_tree(menus, menu.id)
            if child:  
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                    'child': child,
                })
            else:
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                })
    return tree

def list(request):
    temp = Menu.objects.all().order_by('seq')
    result = get_menu_tree(temp)
    postList = Post.objects.all().values('id','title')
    context = {
        'menus': result,
        'postList': postList
    }
    return render(request, 'blog/blog_list.html', context)

def post(request, id):
    temp = Menu.objects.all().order_by('seq')
    result = get_menu_tree(temp)
    post = Post.objects.get(id=id)
    context = {
        'menus': result,
        'post': post,
    }
    return render(request, 'blog/blog_post.html', context)

@login_required(login_url='common:login')
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '등록 완료')
            return redirect('blog:list')
    context = {}
    return render(request, 'blog/blog_form.html', context)

@login_required(login_url='common:login')
def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '수정 완료')
            return redirect('blog:list')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'blog/blog_form.html', context)

@login_required(login_url='common:login')
def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    messages.success(request, '삭제 완료')
    return redirect('blog:list')