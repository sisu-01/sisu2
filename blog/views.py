from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from common.utils import get_client_ip
from .models import Post
from .forms import PostForm
import os
from datetime import datetime

base_template = 'blog/blog_base.html'

def index(request):
    context = {
        'ogTitle': 'ogTitle이다임마',
        'ogDescription': 'ogDescriptionzzzzzzzz',
        'ogImage': None,
        'title': '제목인뒈용',
        'template': 'blog/blog_index.html',
    }
    return render(request, base_template, context)

def list(request, id):
    postList = Post.objects.filter(menu=id).order_by('-insert_date')
    context = {
        'postList': postList,
        'template': 'blog/blog_list.html',
    }
    return render(request, base_template, context)

def post(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
        'template': 'blog/blog_post.html',
    }
    return render(request, base_template, context)

@login_required(login_url='common:login')
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.insert_date = timezone.now()
            post.insert_ip = get_client_ip(request)
            post.save()
            messages.success(request, '등록 완료')
            return redirect('blog:post', id=post.id)
    context = {}
    return render(request, 'blog/blog_form.html', context)

@require_http_methods("POST")
def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload_file = request.FILES['upload']
        date_path = datetime.now().strftime("%Y/%m/%d")
        upload_path = os.path.join(settings.MEDIA_ROOT, 'upload/', date_path)
        os.makedirs(upload_path, exist_ok=True)
        full_path = os.path.join(upload_path, upload_file.name)
        with open(full_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        relative_path = os.path.relpath(full_path, settings.BASE_DIR)
        res = {"url": '/'+relative_path, "uploaded": "1", "fileName": '구화아악'}
        return JsonResponse(res)
    else:
        return '실패 ㅋㅋ'

@login_required(login_url='common:login')
def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.update_date = timezone.now()
            post.update_ip = get_client_ip(request)
            post.save()
            messages.success(request, '수정 완료')
            return redirect('blog:list', id=post.menu)
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
    return redirect('blog:list', id=post.menu)