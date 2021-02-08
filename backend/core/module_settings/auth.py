AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# pylint: disable=line-too-long
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 5}
    },
    {
        'NAME': 'apps.users.validators.ForbiddenCharsValidator',
        'OPTIONS': {
            'forbidden_chars': (
                '\\',
                '~',
                '<',
                '>',
                ' ',
                '\n',
                '\t',
            ),
        }
    },
    {
        'NAME': 'apps.users.validators.IncludeLowerCaseValidator',
    },

]
