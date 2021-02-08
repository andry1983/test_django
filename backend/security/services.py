"""
this module contains functions for generating tokens for the application,
used by default if no virtual env variables are set
"""

import json
import os
import random
import string
import sys

from typing import List, Dict

from django.core.signing import Signer

from backend.helpers.const import SALT, SECURITY_FILE_NAME
from backend.helpers.paths import SECURITY_DIR

SECURE_FILE_PATH = SECURITY_DIR.path(f'./{SECURITY_FILE_NAME}')
SECURE_FILE_PATH_FOR_TEST = SECURITY_DIR.path(f'./test_{SECURITY_FILE_NAME}')

_IS_TEST = (len(sys.argv) > 1 and sys.argv[1] == 'test')
_FILE_PATH = SECURE_FILE_PATH_FOR_TEST if _IS_TEST else SECURE_FILE_PATH


def generate_security_key(length: int = 100) -> str:
    """
    generating random security token
    :param length:
    :return: str
    """
    key: str = ''
    sep: str = ' - '
    key_name: str = 'key'

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    signer = Signer(result_str, sep=sep, salt=SALT or '')
    value = signer.sign(key_name)

    if value:
        _, key = value.split(sep)
    return key


def create_security_file_credentials(keys_list: List[str]) -> None:
    """
    the function generates security tokens for included keys list arguments
     and writes the result in the file example keys_list = ["SECRET_KEY"]
    :param keys_list:
    :return: None
    """

    if not keys_list:
        raise ValueError('parameter keys_list must not be empty!!!')

    tokens_list = {key: generate_security_key() for key in keys_list}
    if not tokens_list:
        raise ValueError('tokens_list must not be empty!!!')
    if not os.path.exists(_FILE_PATH):
        with open(_FILE_PATH, 'w') as file:
            if tokens_list:
                json.dump(tokens_list, indent=2, fp=file)


def read_security_file() -> Dict:
    """
    reads security tokens from security file
    :return:
    """
    result: Dict = dict()

    if os.path.exists(_FILE_PATH):
        with open(_FILE_PATH, 'r') as file:
            try:
                file_data = json.load(fp=file, object_hook=dict)
            except (json.JSONDecodeError, ValueError) as e:
                file.seek(0)
                file_content = file.read()
                if not file_content:
                    msg: str = 'The security file is empty.Please re-create ' \
                               'your security credentials'
                else:
                    msg: str = f'\n\tFile content: {file_content}\n\tError:{e}'
                raise ValueError(msg) from e
            else:
                result.update(file_data)
    return result


def update_security_file(keys_list: List[str]) -> Dict[str, str]:
    """
    updates the security file if it exists, if it doesn't exist create
     this file
    :param keys_list:
    :return:
    """
    if not keys_list:
        raise ValueError('parameter keys_list must not be empty!!!')

    if not os.path.exists(_FILE_PATH):
        create_security_file_credentials(keys_list=keys_list)
        return read_security_file()

    new_tokens: Dict[str, str] = dict()
    data_security_file: Dict[str, str] = read_security_file()
    for token_name in keys_list:
        if token_name not in data_security_file:
            new_tokens[token_name] = generate_security_key()
    data_security_file.update(new_tokens)
    if data_security_file:
        with open(_FILE_PATH, 'w') as file:
            json.dump(data_security_file, indent=2, fp=file)
    return data_security_file
