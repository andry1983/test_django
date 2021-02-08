import os

from backend.helpers.env_args import env
from backend.helpers.paths import LOG_DIR

if not os.path.exists(LOG_DIR.root):
    os.makedirs(LOG_DIR.root)

DEBUG = env('DJANGO_DEBUG')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(levelname)s %(asctime)s %(name)s %(pathname)s'
                      ' %(funcName)s %(lineno)d \n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'medium': {
            'format': '[%(asctime)s] [%(levelname)s %(module)s %(lineno)d]'
                      ' %(message)s %(exc_info)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'medium',
        },
        'logfile': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR.path('info.log').root,
            'maxBytes': 1024 * 1024 * 5,  # 5mb
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'log_file_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR.path('errors.log').root,
            'maxBytes': 1024 * 1024 * 5,  # 5mb
            'backupCount': 2,
            'formatter': 'medium',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'log_file_warning'],
            'level': 'WARN',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARN',
            'propagate': False,
        },
        'file_console_logger': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True
        },
        'file_logger': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

if env.bool('DJANGO_DEBUG_SQL'):
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['sql_console'],
        'propagate': False,
        'level': 'DEBUG',
    }
    LOGGING['formatters'].update(
        {
            'sql': {
                '()': 'django_sqlformatter.SqlFormatter',
                'format': '%(levelname)s[%(server_time)s]\n %(message)s',
            }
        })
    LOGGING['handlers'].update(
        {
            'sql_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'sql',
            }
        })
