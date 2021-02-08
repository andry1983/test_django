from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from backend.helpers.forms import (
    ERROR_CSS_CLASS,
    WIDGET_TYPES,
    add_css_class_to_fields_widget,
    add_error_css_class_to_form_fields_widget, set_default_placeholder,
)

# pylint: disable=import-error,no-name-in-module
from apps.users.models import User, UserReferrerCode
from core.settings import REGISTRATION_WITHOUT_REFERRER_CODE


class UserAuthenticationForm(AuthenticationForm):
    error_css_class = ERROR_CSS_CLASS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_css_class_to_fields_widget(self.fields, 'form-control',
                                       widget_types=WIDGET_TYPES)
        set_default_placeholder(self.fields)

    def full_clean(self):
        super().full_clean()
        add_error_css_class_to_form_fields_widget(self)


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), max_length=254, required=True)
    first_name = forms.CharField(label=_('first name'), required=True)
    last_name = forms.CharField(label=_('last name'), required=False)
    referral_code = forms.CharField(label=_('referral code'), help_text='',
                                    required=False)
    error_css_class = ERROR_CSS_CLASS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_css_class_to_fields_widget(self.fields, 'form-control required',
                                       widget_types=WIDGET_TYPES)
        set_default_placeholder(self.fields)

    @property
    def clean_referral_code(self):
        user_count = User.objects.filter(is_superuser=False).count()
        code = self.cleaned_data.get('referral_code')
        if not code and user_count >= REGISTRATION_WITHOUT_REFERRER_CODE:
            raise ValidationError(_('A referrer code is required'))
        if code:
            error_msg = _('A referrer code is incorrect')
            try:
                code_exist = UserReferrerCode.objects.filter(
                    code=code).exists()
            except ValidationError as e:
                raise ValidationError(error_msg) from e
            if not code_exist:
                raise ValidationError(error_msg)
        return lambda: code

    def full_clean(self):
        super().full_clean()
        add_error_css_class_to_form_fields_widget(self)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
