from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from .forms import *
from pathlib import Path
from dataclasses import dataclass, asdict
import urllib.request
import json, os, environ

BASE_DIR = Path(__file__).resolve().parent.parent
temp = os.environ.setdefault('DJANGO_ENV', 'sisu2_local.env')
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, temp)
)
key = env('MOVIE')

@dataclass
class Response:
    status: bool
    message: str
    data: dict

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
    movie 영화 등록
    """
    form = MovieForm(request.POST)
    if form.is_valid():
        movie = form.save(commit=False)
        #movie.user
        movie.insert_date = timezone.now()
        movie.insert_ip = '127.0.0.1'
        #movie.insert_ip = '으아아아 IP 뜯기~!~'
        movie.save()
        res = Response(status=True,message='성공',data=None)
    else:
        res = Response(status=False,message='실패',data=dict(form.errors))

    return JsonResponse(asdict(res))

@require_http_methods("POST")
def select(request):
    """
    movie 영화 불러오기
    """
    try:
        param = json.loads(request.body)
        movie = Movie.objects.get(pk=param['movie_id'])
        from django.forms.models import model_to_dict
        res = Response(status=True,message='성공',data=model_to_dict(movie))
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))