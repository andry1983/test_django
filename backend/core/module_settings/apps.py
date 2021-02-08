# APPS
from backend.helpers.env_args import env

THIRD_PARTY_APPS = (
    'corsheaders',
    'rules'
)

LOCAL_APPS = (
    'core',
    'apps.users'
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
)

if env('DJANGO_ADMIN'):
    DJANGO_APPS += ('django.contrib.admin',)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
