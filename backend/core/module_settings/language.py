from django.utils.translation import gettext_lazy as _

from backend.helpers.env_args import env

# Internationalization
LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = []
for lang in env.list('DJANGO_LANGUAGES'):
    lang_key, translate = lang.split(':')
    LANGUAGES += [(lang_key, _(translate))]
