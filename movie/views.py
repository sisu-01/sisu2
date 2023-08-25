from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render
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

# Create your views here.
def index(request):
    return render(request, 'movie/movie.html')

@require_http_methods("POST")
def search(request):
    #res 중복되는거 해결해보자
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
            result = 1
            mess = 'success'
        else:
            result = 0
            mess = 'Error Code : '+rescode
            movieList = None
        res = {
            'result': result,
            'mess': mess,
            'movie_list': movieList
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            'result': 0,
            'mess': e,
            'movie_list': None
        }
        return JsonResponse(res)