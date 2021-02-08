DEFAULT_LANGUAGE_CODE = 'en'
DEFAULT_STATIC_NAME = 'static'
DEFAULT_ENV_SETTING_FILE_NAME = '.env'
DEFAULT_DJANGO_TEST_DB_NAME = 'test_db'
DEFAULT_POSTGRESQL_PORT = 5432
DEFAULT_DJANGO_SERVER_PORT = 8000
SALT = 'django-test'
SECURITY_FILE_NAME = 'app_security_keys.json'

'''keys for generating tokens for the application, used by default if virtual
env variables are not set'''
REQUIRED_SECURITY_APP_TOKEN = ['DJANGO_SECRET_KEY']
