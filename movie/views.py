from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
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

# 여기에서 뷰를 생성하세요.
def index(request):
    """
    movie 첫화면
    """
    movieList = Movie.objects.all().order_by('-date')
    form = MovieForm()
    context = {
        'form': form,
        'movieList': movieList,
    }
    return render(request, 'movie/movie.html', context)

@require_http_methods("POST")
def search(request):
    """
    movie KOBIS API
    """
    try:
        param = json.loads(request.body)
        movieNm = urllib.parse.quote(param['movieNm'])
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
        url = url+"?key="+key
        url = url+"&movieNm="+movieNm
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            movieList = json.loads(response_body.decode('utf-8'))['movieListResult']['movieList']
            status = True
            message = 'success'
        else:
            status = False
            message = 'Error Code : '+rescode
            movieList = None
        res = Response(status=status,message=message,data=movieList)
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def insert(request):
    """
    movie 등록&수정
    """
    try:
        movieId = request.POST.get('id')
        if movieId == '':
            form = MovieForm(request.POST)
        else:
            instMovie = Movie.objects.get(pk=movieId)
            form = MovieForm(request.POST, instance=instMovie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.weekday = movie.date.weekday()
            if movieId == '':
                #movie.user
                movie.insert_date = timezone.now()
                movie.insert_ip = get_client_ip(request)
            else:
                movie.update_date = timezone.now()
                movie.update_ip = get_client_ip(request)
            movie.save()
            res = Response(status=True,message='성공',data=None)
        else:
            res = Response(status=False,message='The form is invalid.',data=dict(form.errors))
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def select(request):
    """
    movie 불러오기
    """
    try:
        param = json.loads(request.body)
        movie = Movie.objects.get(pk=param['movie_id'])
        res = Response(status=True,message='성공',data=model_to_dict(movie))
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))

@require_http_methods("POST")
def delete(request):
    """
    movie 삭제
    """
    try:
        param = json.loads(request.body)
        movie = get_object_or_404(Movie, pk=param['movie_id'])
        movie.delete()
        res = Response(status=True,message='삭제 성공',data=None)
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))