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

# 여기에서 뷰를 생성하세요.
def index(request):
    """
    movie 첫화면
    """
    """
    import math
    import time
    start1 = time.time()
    cnt1 = 0
    end1 = time.time()
    result1 = (end1-start1)*100
    from django.db.models.functions import ExtractYear
    from django.db.models import Count
    #구 로직
    movieList1 = Movie.objects.all().order_by('-date', '-id')
    dateList1 = Movie.objects.annotate(year=ExtractYear('date')).values('year').annotate(total=Count('*')).order_by('-year')
    for i in dateList1:
        print(i['year'], i['total'])
        for j in movieList1:
            if i['year'] == j.date.year:
                print(j.title)
    from django.db.models.functions import ExtractYear
    #신 로직
    movieList2 = Movie.objects.all().order_by('-date', '-id')
    dateList2 = Movie.objects.annotate(year=ExtractYear('date')).values('year').order_by('-year')
    temp = {}
    for date in dateList2:
        temp[date['year']] = []
    for movie in movieList2:
        temp[movie.date.year].append(movie.title)
    for i in temp:
        print(i, len(temp[i]))
        for j in temp[i]:
            print(j)
    """
    #황보 로직
    movieList = Movie.objects.all().order_by('-date', '-id')
    temp = {}
    total = len(movieList)
    for movie in movieList:
        year = movie.date.year
        if (not year in temp):
            temp[year] = []
        temp[movie.date.year].append({
            'id': movie.id,
            'title': movie.title,
            'count': total,
        })
        total -= 1
    form = MovieForm()
    context = {
        'form': form,
        'movieList': movieList,
        'temp': temp,
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
        oldPoster = ''
        oldTHumb = ''
        movieId = request.POST.get('id')
        if movieId == '':
            form = MovieForm(request.POST, request.FILES)
        else:
            instance = Movie.objects.get(pk=movieId)
            form = MovieForm(request.POST, request.FILES, instance=instance)
            oldPoster = str(instance.poster)
            oldTHumb = str(instance.thumbnail)
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
            if(oldPoster != str(movie.poster)):
                if os.path.isfile(Path(settings.MEDIA_ROOT, oldPoster)):
                    os.remove(Path(settings.MEDIA_ROOT, oldPoster))
            if(oldTHumb != str(movie.thumbnail)):
                if os.path.isfile(Path(settings.MEDIA_ROOT, oldTHumb)):
                    os.remove(Path(settings.MEDIA_ROOT, oldTHumb))
            data = Movie.objects.filter(pk=movie.id).values()[0]
            res = Response(status=True,message='성공',data=data)
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
        movie = Movie.objects.filter(pk=param['id']).values()[0]
        res = Response(status=True,message='성공',data=movie)
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
        movie = get_object_or_404(Movie, pk=param['id'])
        if os.path.isfile(Path(settings.MEDIA_ROOT, str(movie.poster))):
            os.remove(Path(settings.MEDIA_ROOT, str(movie.poster)))
        if os.path.isfile(Path(settings.MEDIA_ROOT, str(movie.thumbnail))):
            os.remove(Path(settings.MEDIA_ROOT, str(movie.thumbnail)))
        movie.delete()
        res = Response(status=True,message='삭제 성공',data=None)
    except Exception as e:
        res = Response(status=False,message=str(e),data=None)
    return JsonResponse(asdict(res))