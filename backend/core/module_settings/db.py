from backend.helpers.env_args import env

DJANGO_DB_NAME = env('DJANGO_DB_NAME')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DJANGO_DB_NAME,
        'USER': env('DJANGO_USER_DB'),
        'PASSWORD': env('DJANGO_DB_PASS'),
        'HOST': env('DJANGO_DB_HOST'),
        'PORT': env('DJANGO_DB_PORT'),
        'TEST': {
            'NAME': env('DJANGO_TEST_DB_NAME'),
        },
    }
}
