import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class BaseValidator:
    pass


class ForbiddenCharsValidator(BaseValidator):
    ERROR_MESSAGE = 'You can not use "{}" in password.'

    def __init__(self, forbidden_chars=()):
        self.forbidden_chars = forbidden_chars

    def validate(self, password, user=None):
        for char in self.forbidden_chars:
            if char in password:
                raise ValidationError(
                    _(self.ERROR_MESSAGE.format(char)),
                    code='forbidden_characters_used',
                    params={'forbidden_characters': self.forbidden_chars},
                )

    def get_help_text(self):
        chars = ', '.join(self.forbidden_chars)
        return _(self.ERROR_MESSAGE.format(chars))


class IncludeLowerCaseValidator(BaseValidator):
    ERROR_MESSAGE = 'You must use at least one lowercase english letter.'

    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(_(self.ERROR_MESSAGE))

    def get_help_text(self):
        return _(self.ERROR_MESSAGE)
