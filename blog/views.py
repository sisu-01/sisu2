from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from common.utils import get_client_ip, Response
from .models import BlogTree, BlogPost, BlogComment
from .forms import TreeForm, PostForm, CommentForm
from dataclasses import asdict, dataclass
from datetime import datetime
import os, json

base_template = 'blog/blog_base.html'
paginate_by = 10
page_btn = 5

@dataclass
class OpenGraph():
    title: str
    desc: str
    image: str

def index(request):
    context = {
        'template': 'blog/blog_index.html',
        'og': asdict(OpenGraph('블로그', '블로그임둥~ 엌~!', None)),
    }
    return render(request, base_template, context)

def get_post_list(request, id):
    page = int(request.GET.get('page',1))

    if id == 'all':
        tree_title = '전체보기'
        post_list = BlogPost.objects.all().order_by('-insert_date')
    elif id == 'null':
        tree_title = '고아들'
        post_list = BlogPost.objects.filter(tree=None).order_by('-insert_date')
    else:
        trees = BlogTree.objects.all().order_by('seq')
        tree_title = trees.get(pk=id).title
        tree_list = find_child(trees, int(id))
        post_list = BlogPost.objects.filter(tree__in=tree_list).order_by('-insert_date')
    
    if not request.user.is_authenticated:
        post_list = post_list.filter(is_public=1)

    p = Paginator(post_list, paginate_by)
    page_obj = p.get_page(page)

    slicing = (page-1)//page_btn*page_btn
    paging = [*p.page_range]

    context = {
        'post_list': page_obj,
        'paging': paging[slicing:slicing+page_btn],
        'slicing': slicing,
        'page_btn': page_btn,
        'tree_title': tree_title,
        'template': 'blog/blog_list.html',
        'og': asdict(OpenGraph('블로그 목록', '무슨 글을 봐야하지;;', None)),
    }
    return render(request, base_template, context)

def find_child(menus, parent):
    id_list = []
    id_list.append(parent)
    for i in menus:
        if i.parent_id == parent:
            id_list.extend(find_child(menus,i.id))
    return id_list

def get_post(request, id):
    post = BlogPost.objects.get(id=id)
    if not request.user.is_authenticated and not post.is_public:
        context = {
            'template': 'blog/blog_forbidden.html',
            'og': asdict(OpenGraph('접.근.금.지', '비공개 처리된 글입니다..ㅠ', None)),
        }
        return render(request, base_template, context)
    else:
        post.view_count += 1
        post.save()
        cmt_list = BlogComment.objects.filter(post=post.id)
        """
        from django.utils.html import strip_tags
        print(post.content[:60])
        print(strip_tags(post.content[:100]))
        temp = strip_tags(post.content[:100])
        temp = temp.replace(chr(13),'')
        temp = temp.replace(chr(10),'')
        //수정 나중에 os description 확인해보셈
        """
        context = {
            'post': post,
            'cmt_list': cmt_list,
            'template': 'blog/blog_post.html',
            'og': asdict(OpenGraph(post.title, post.content[:60], post.thumbnail)),
        }
        return render(request, base_template, context)

@login_required(login_url='common:login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thumbnail = check_thumbnail(post.content)
            post.insert_date = timezone.now()
            post.insert_ip = get_client_ip(request)
            post.save()
            messages.success(request, '등록 완료')
            return redirect('blog:get_post', id=post.id)
    context = {}
    return render(request, 'blog/blog_form.html', context)

@login_required(login_url='common:login')
def update_post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.thumbnail = check_thumbnail(post.content)
            post.update_date = timezone.now()
            post.update_ip = get_client_ip(request)
            post.save()
            messages.success(request, '수정 완료')
            return redirect('blog:get_post', id=post.id)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'blog/blog_form.html', context)

def check_thumbnail(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    first_image = soup.find('img')  # 첫 번째 <p> 엘리먼트를 찾음
    if first_image:
        return first_image['src']
    else:
        return None

@require_http_methods("POST")
def ckeditor_upload_image(request):
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
        #//수정 os가 윈도우에서는 /를 \로 바꾸거든? 리눅스에서도 그러는지 보자고.
        res = {"url": '/'+relative_path, "uploaded": "1", "fileName": '구화아악'}
        #//수정 구와아악 fileName이 뭐하는 건지 파악해 uploaded 랑 ㅇㅋ?
        return JsonResponse(res)
    else:
        return '실패'

@login_required(login_url='common:login')
def delete_post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    post.delete()
    messages.success(request, '삭제 완료')
    return redirect('blog:post_list', id=post.id)

@require_http_methods("POST")
def get_cmt(request):
    try:
        param = json.loads(request.body)
        cmt_list = BlogComment.objects.filter(post=param['postId']).values()
        comment = ''
        for i in cmt_list:
            comment += '<div class="comment">'
            comment += f'<span>이름:{i["nickname"]}</span>'
            if i['is_authenticated']:
                comment += ' (주인이다!)'
            comment += f'<br/><span>내용:{i["content"]}</span>'
            if request.user.is_authenticated:
                comment += f' <button class="delete-button" post-id="{str(i["id"])}">수퍼x</button>'
            elif not request.user.is_authenticated and not i['is_authenticated']:
                comment += f' <button type="button" class="modal-button" modal-id="{str(i["id"])}">모달x</button>'
            comment += '</div><hr>'
        res = Response(True, '성공', comment)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def create_cmt(request):
    try:
        #copy()를 주는 이유는 그냥 POST는 immutable, 수정 불가능이라서..
        #만약 로그인시 nickname 자동 추가, 비번 필수 뺴려고..
        form = CommentForm(request.POST.copy(), user=request.user)
        if form.is_valid():
            cmt = form.save(commit=False)
            cmt.is_authenticated = request.user.is_authenticated
            cmt.insert_date = timezone.now()
            cmt.insert_ip = get_client_ip(request)
            cmt.save()
            res = Response(True, '성공', None)
        else:
            res = Response(False, 'The form is invalid.', dict(form.errors))
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def delete_cmt(request):
    try:
        param = json.loads(request.body)
        print(param)
        cmt = get_object_or_404(BlogComment, pk=param['id'])
        if request.user.is_authenticated:
            cmt.delete()
            res = Response(True, '수퍼 삭제 성공', None)
        else:
            if cmt.is_authenticated:
                res = Response(False, '왜 로그인 댓글을 지우시려고;;', None)
            else:
                if cmt.password != param['password']:
                    res = Response(False, '비번이 다름;;', None)
                else:
                    cmt.delete()
                    res = Response(True, '텅과!', None)
                    #//실패인데도 Res에 True라고 적은게 있나 확인.
    except Exception as e:
        res = Response(False, str(e), None)
        #//수정 에러 로그 자세히 주면 해킹당해..
        #//172번 댓글이 없다고 에러를 뿜으면 어카냐..
    return JsonResponse(asdict(res))

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
def save_tree(request):
    try:
        id = request.POST.get('id')
        if id == '':
            form = TreeForm(request.POST)
        else:
            instance = BlogTree.objects.get(pk=id)
            form = TreeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            res = Response(True, '등록 성공', None)
        else:
            res = Response(False, 'The form is invalid.', None)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def select_tree(request):
    try:
        param = json.loads(request.body)
        movie = BlogTree.objects.filter(pk=param['id']).values('id','title','seq','parent')[0]
        res = Response(True, '', movie)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def delete_tree(request):
    try:
        param = json.loads(request.body)
        tree = get_object_or_404(BlogTree, pk=param['id'])
        tree.delete()
        res = Response(True, '삭제 성공', None)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))