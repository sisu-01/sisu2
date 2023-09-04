"""
프로젝트의 URL 구성입니다.

'urlpatterns' 목록은 URL을 뷰로 라우팅합니다. 자세한 내용은 다음을 참조하세요.
     https://docs.djangoproject.com/en/4.2/topics/http/urls/
예:
기능 보기
     1. 가져오기 추가: my_app 가져오기 보기에서
     2. urlpatterns에 URL을 추가합니다: path('', views.home, name='home')
클래스 기반 보기
     1. 가져오기 추가: from other_app.views import 홈
     2. urlpatterns에 URL을 추가합니다: path('', Home.as_view(), name='home')
다른 URLconf 포함
     1. include() 함수를 가져옵니다. django.urls에서 include, path를 가져옵니다.
     2. urlpatterns에 URL을 추가합니다: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('blog/', include('blog.urls')),
    path('movie/', include('movie.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)