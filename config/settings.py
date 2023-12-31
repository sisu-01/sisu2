"""
프로젝트에 대한 Django 설정.

Django 4.2.4를 사용하여 'django-admin startproject'에 의해 생성되었습니다.

이 파일에 대한 자세한 내용은 다음을 참조하십시오.
https://docs.djangoproject.com/en/4.2/topics/settings/

설정 및 해당 값의 전체 목록은 다음을 참조하세요.
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
from pathlib import Path

# 다음과 같이 프로젝트 내부에 경로를 빌드합니다: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# env 파일 설정입니다
temp = os.environ.setdefault('DJANGO_ENV', 'sisu2_local.env')
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, temp)
)

# 빠른 시작 개발 설정 - 프로덕션에 적합하지 않음
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/ 참조

# 보안 경고: 생산에 사용된 비밀 키를 비밀로 유지하십시오!
SECRET_KEY = env('SECRET_KEY')

# 보안 경고: 프로덕션에서 디버그를 켠 상태로 실행하지 마십시오!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')


# 애플리케이션 정의

INSTALLED_APPS = [
    'common',
    'blog',
    'movie',
    'captcha',
    'django.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('NAME'),
        'USER': env('USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT'),
        'OPTIONS' : {
            'charset' : 'utf8mb4'
        }
    }
}


# 비밀번호 확인
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 국제화
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# 로그인/로그아웃
# https://docs.djangoproject.com/en/4.2/ref/settings/#login-redirect-url

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# 세션 만료 시간
# https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-age

#SESSION_COOKIE_AGE = 2주 1209600 기본
# 1년 31536000 한달 2628000 일주일 604800


# 캡챠 설정
# https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
 
CAPTCHA_FONT_SIZE = 26

CAPTCHA_IMAGE_SIZE = (90,33)

#CAPTCHA_LETTER_ROTATION = None

CAPTCHA_FOREGROUND_COLOR = '#ff0000'

CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs', 'captcha.helpers.noise_dots',)

CAPTCHA_LENGTH = 2

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'


# Static 파일 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# Media 파일 (Movie, Thumbnail, Blog)
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_URL = '/media/'

#MEDIA_ROOT = BASE_DIR / 'media'
#os path join 은 무슨 차이일까?
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 여기 설정된된 메모리 사이즈보다 작으면 InMemoryUploadedFile,
# 크면 TemporaryUploadedFile로 업로드 하는데,
# Temp로 하면 에러가 나..
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-FILE_UPLOAD_MAX_MEMORY_SIZE
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760 # Default: 2621440 (i.e. 2.5 MB).


# 기본 기본 키 필드 유형
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
