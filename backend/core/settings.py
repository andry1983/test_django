# when importing, debug settings should be first
from backend.helpers.env_args import env
from backend.core.module_settings.debug import *

from backend.core.module_settings.apps import *
from backend.core.module_settings.auth import *
from backend.core.module_settings.cors_mimetypes import *
from backend.core.module_settings.db import *
from backend.core.module_settings.email import *
from backend.core.module_settings.language import *
from backend.core.module_settings.logger import *
from backend.core.module_settings.middlewares import *
from backend.core.module_settings.static import *
from backend.core.module_settings.templates import *

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

ACCOUNT_DEFAULT_HTTP_PROTOCOL = env('DJANGO_DEFAULT_HTTP_PROTOCOL')

# hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]

DEBUG = env('DJANGO_DEBUG')

DJANGO_ADMIN = env('DJANGO_ADMIN')

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

SERVER_PORT = env('DJANGO_PORT')
SERVER_HOST = env('HOST')
REGISTRATION_WITHOUT_REFERRER_CODE = env(
    'USER_COUNT_REGISTRATION_WITHOUT_REFERRER_CODE')
BASE_DIR = ROOT_DIR.root
