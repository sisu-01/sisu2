from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from dataclasses import asdict
from .models import *
from .forms import *
from common.utils import get_client_ip, Response
from pathlib import Path
import urllib.request
import json, os, environ

BASE_DIR = Path(__file__).resolve().parent.parent
temp = os.environ.setdefault('DJANGO_ENV', 'sisu2_local.env')
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, temp)
)
key = env('MOVIE')

def index(request):
    """
    첫 화면
    """
    movie_list = Movie.objects.all().order_by('-date', '-id')
    toc = {}
    total = len(movie_list)
    for movie in movie_list:
        year = movie.date.year
        if (not year in toc):
            toc[year] = []
        toc[movie.date.year].append({
            'id': movie.id,
            'title': movie.title,
            'count': total,
        })
        total -= 1
    form = MovieForm()
    og = {
        'title': '포토티켓일지도?',
        'desc': '영화들 ㅋㅋㅋㅋㅋㅋ',
        'image': movie_list[0].thumbnail,
    }
    context = {
        'form': form,
        'movie_list': movie_list,
        'toc': toc,
        'og': og,
    }
    return render(request, 'movie/movie.html', context)

@require_http_methods("POST")
def call_kobis_api(request):
    """
    KOBIS API 호출
    """
    try:
        param = json.loads(request.body)
        movie_name = urllib.parse.quote(param['movieName'])
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"+"?key="+key+"&movieNm="+movie_name
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode == 200):
            status = True
            message = '성공'
            response_body = response.read()
            movie_list = json.loads(response_body.decode('utf-8'))['movieListResult']['movieList']
        else:
            status = False
            message = '에러 코드: '+rescode
            movie_list = None
        res = Response(status, message, movie_list)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def save_movie(request):
    """
    등록&수정
    """
    try:
        old_poster = ''
        old_thumb = ''
        id = request.POST.get('id')
        if id == '':
            form = MovieForm(request.POST, request.FILES)
        else:
            instance = Movie.objects.get(pk=id)
            form = MovieForm(request.POST, request.FILES, instance=instance)
            old_poster = str(instance.poster)
            old_thumb = str(instance.thumbnail)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.weekday = movie.date.weekday()
            if id == '':
                movie.insert_date = timezone.now()
                movie.insert_ip = get_client_ip(request)
            else:
                movie.update_date = timezone.now()
                movie.update_ip = get_client_ip(request)
            movie.save()
            if(old_poster != str(movie.poster)):
                if os.path.isfile(Path(settings.MEDIA_ROOT, old_poster)):
                    os.remove(Path(settings.MEDIA_ROOT, old_poster))
            if(old_thumb != str(movie.thumbnail)):
                if os.path.isfile(Path(settings.MEDIA_ROOT, old_thumb)):
                    os.remove(Path(settings.MEDIA_ROOT, old_thumb))
            data = Movie.objects.filter(pk=movie.id).values()[0]
            res = Response(True, '성공', data)
        else:
            res = Response(False, 'The form is invalid.', dict(form.errors))
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def get_movie(request):
    """
    영화 조회
    """
    try:
        param = json.loads(request.body)
        movie = Movie.objects.filter(pk=param['id']).values()[0]
        res = Response(True, '성공', movie)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def delete_movie(request):
    """
    movie 삭제
    """
    try:
        param = json.loads(request.body)
        movie = get_object_or_404(Movie, pk=param['id'])
        if os.path.isfile(Path(settings.MEDIA_ROOT, str(movie.poster))):
            os.remove(Path(settings.MEDIA_ROOT, str(movie.poster)))
        if os.path.isfile(Path(settings.MEDIA_ROOT, str(movie.thumbnail))):
            os.remove(Path(settings.MEDIA_ROOT, str(movie.thumbnail)))
        movie.delete()
        res = Response(True, '삭제 성공', None)
    except Exception as e:
        res = Response(False, str(e), None)
    return JsonResponse(asdict(res))