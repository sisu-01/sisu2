from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from common.utils import get_client_ip, Response
from .models import BlogTree, BlogPost
from .forms import PostForm, TreeForm
from dataclasses import asdict
from datetime import datetime
import os, json

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

def listz(request, id):
    trees = BlogTree.objects.all().order_by('seq')
    tree_title = trees.get(pk=id).title
    tree_list = find_child(trees, id)
    postList = BlogPost.objects.filter(tree__in=tree_list).order_by('-insert_date')
    context = {
        'postList': postList,
        'tree_title': tree_title,
        'template': 'blog/blog_list.html',
    }
    return render(request, base_template, context)

def find_child(menus, parent):
    id_list = []
    id_list.append(parent)
    for i in menus:
        if i.parent_id == parent:
            id_list.extend(find_child(menus,i.id))
    return id_list

def post(request, id):
    post = BlogPost.objects.get(id=id)
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
    post = get_object_or_404(BlogPost, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.update_date = timezone.now()
            post.update_ip = get_client_ip(request)
            post.save()
            messages.success(request, '수정 완료')
            return redirect('blog:list', id=post.tree)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'blog/blog_form.html', context)

@login_required(login_url='common:login')
def delete(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    post.delete()
    messages.success(request, '삭제 완료')
    return redirect('blog:list', id=post.tree)

@login_required(login_url='common:login')
def tree(request):
    context = {}
    return render(request, 'blog/blog_tree.html', context)

@require_http_methods("POST")
def get_tree(request):
    try:
        menus = list(BlogTree.objects.all().order_by('seq').values())
        res = Response(True,'',menus)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def create_tree(request):
    try:
        id = request.POST.get('id')
        if id == '':
            form = TreeForm(request.POST)
        else:
            instance = BlogTree.objects.get(pk=id)
            form = TreeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            res = Response(True,'등록 성공',None)
        else:
            res = Response(False,'The form is invalid.',None)
    except Exception as e:
        res = Response(False,str(e),None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def select_tree(request):
    try:
        param = json.loads(request.body)
        movie = BlogTree.objects.filter(pk=param['id']).values('id','title','seq','parent')[0]
        res = Response(True,'',movie)
    except Exception as e:
        res = Response(False,str(e),None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def delete_tree(request):
    try:
        param = json.loads(request.body)
        print(param)
        tree = get_object_or_404(BlogTree, pk=param['id'])
        tree.delete()
        res = Response(True,'삭제 성공',None)
    except Exception as e:
        res = Response(False,str(e),None)
    return JsonResponse(asdict(res))