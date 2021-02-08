from backend.apps.users.rules.type import is_admin
from backend.core.module_settings import apps
from backend.core.module_settings import middlewares
from backend.helpers.env_args import env

# debug
if env('DJANGO_DEBUG'):
    # DEBUG CODE
    USE_SILK = env('DJANGO_USE_SILK')
    SILK_AUTHORIZE = env('DJANGO_SILK_AUTHORIZE')

    if USE_SILK:
        apps.INSTALLED_APPS += (
            'silk',
        )
        middlewares.MIDDLEWARE += (
            'silk.middleware.SilkyMiddleware',
        )
        # Turn on profiling for requests.
        SILKY_PYTHON_PROFILER = True
        # Number of requests which are monitored.
        SILKY_INTERCEPT_PERCENT = 100
        # Only keep the n newest requests
        # Wipe all with `python manage.py silk_clear_request_log`
        SILKY_MAX_RECORDED_REQUESTS = 1000
        SILKY_AUTHENTICATION = SILK_AUTHORIZE  # User must login
        if SILK_AUTHORIZE:
            SILKY_AUTHORISATION = SILK_AUTHORIZE  # User must have permissions
            SILKY_PERMISSIONS = not is_admin
        # Measure the overhead introduced by silk
        SILKY_META = True
        SILKY_MAX_REQUEST_BODY_SIZE = 10000
        SILKY_MAX_RESPONSE_BODY_SIZE = 10000

    USE_DEBUG_TOOLBAR = env.bool('DJANGO_USE_DEBUG_TOOLBAR')

    if USE_DEBUG_TOOLBAR:
        # disable due to error in SQL toolbar (Expl | Sel)
        # if USE_SILK:
        #     raise Warning("Please disable Django silk debugging!!!")

        middleware = 'debug_toolbar.middleware.DebugToolbarMiddleware'
        middlewares.MIDDLEWARE += (
            middleware,
        )
        apps.INSTALLED_APPS += (
            'debug_toolbar',
        )
        DEBUG_TOOLBAR_CONFIG = {
            'DISABLE_PANELS': [
                'debug_toolbar.panels.redirects.RedirectsPanel',
            ],
            'SHOW_TEMPLATE_CONTEXT': True,
            'SHOW_TOOLBAR_CALLBACK': lambda request: True,
        }

        DEBUG_TOOLBAR_PATCH_SETTINGS = False

        INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')
