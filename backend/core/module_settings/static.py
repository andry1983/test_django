from backend.helpers.env_args import env
from backend.helpers.paths import ROOT_DIR

STATIC_NAME = env('STATIC_NAME')
STATIC_URL = f'/{STATIC_NAME}/'
STATIC_ROOT = ROOT_DIR.path(STATIC_NAME).root

# STATICFILES_DIRS = (
#     PROJECT_DIR.path(STATIC_NAME).root,
# )
