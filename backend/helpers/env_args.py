import os
import environ

from typing import Dict, List

from backend.helpers.const import (
    DEFAULT_DJANGO_SERVER_PORT,
    DEFAULT_DJANGO_TEST_DB_NAME,
    DEFAULT_ENV_SETTING_FILE_NAME,
    DEFAULT_LANGUAGE_CODE,
    DEFAULT_POSTGRESQL_PORT,
    DEFAULT_STATIC_NAME,
    REQUIRED_SECURITY_APP_TOKEN,
)

from backend.helpers.paths import ENV_BACKEND_DIR, COVERAGE_RC_FILE_PATH
from backend.security.services import (
    create_security_file_credentials,
    read_security_file,
    update_security_file,
)

env = environ.Env(
    COVERAGE_RCFILE=(str, COVERAGE_RC_FILE_PATH),
    DJANGO_ADMIN=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_CORS_ORIGIN_WHITELIST=(list, []),
    DJANGO_DB_HOST=(str, ''),
    DJANGO_DB_NAME=(str, ''),
    DJANGO_DB_PASS=(str, ''),
    DJANGO_DB_PORT=(int, DEFAULT_POSTGRESQL_PORT),
    DJANGO_TEST_DB_NAME=(str, DEFAULT_DJANGO_TEST_DB_NAME),
    DJANGO_DEBUG=(bool, False),
    DJANGO_DEBUG_SQL=(bool, False),
    DJANGO_PORT=(int, DEFAULT_DJANGO_SERVER_PORT),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_TEST_RUN=(bool, False),
    DJANGO_USER_DB=(str, ''),
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_USE_SILK=(bool, False),
    DJANGO_SILK_AUTHORIZE=(bool, True),
    EMAIL_HOST=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
    EMAIL_HOST_USER=(str, None),
    EMAIL_PORT=(int, 465),
    HOST=(str, ''),
    LANGUAGE_CODE=(str, DEFAULT_LANGUAGE_CODE),
    STATIC_NAME=(str, DEFAULT_STATIC_NAME),
    USER_COUNT_REGISTRATION_WITHOUT_REFERRER_CODE=(int, 5),
)

ENV_FILE_PATH = ENV_BACKEND_DIR.path(f'./{DEFAULT_ENV_SETTING_FILE_NAME}').root
environ.Env.read_env(ENV_FILE_PATH)


def set_required_tokens() -> None:
    """
    check if the required security tokens are installed in the environment and
    the tokens are not empty. if there are no tokens or tokens exist but they
    are empty, the function generates default values
    :return:
    """
    required_token_list: List[str] = REQUIRED_SECURITY_APP_TOKEN
    missing_tokens: List[str] = [token_name for token_name in
                                 required_token_list if
                                 not environ.Env().get_value(token_name,
                                                             default=None)]

    if missing_tokens:
        create_security_file_credentials(keys_list=missing_tokens)
        generated_tokens: Dict[str, str] = read_security_file()
        were_tokens_create: bool = not bool(
            set(missing_tokens) - set(generated_tokens.keys()))
        if not were_tokens_create:
            try:
                update_security_file(missing_tokens)
            except Exception as e:
                msg = f'\tsecurity tokens could not be generated;\n\tError:{e}'
                raise Exception(msg) from e
            else:
                set_required_tokens()
        for token_name, token_value in generated_tokens.items():
            if token_name in missing_tokens:
                os.environ[token_name] = token_value


set_required_tokens()
