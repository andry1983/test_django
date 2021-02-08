import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from backend.apps.users.managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(
        _('Email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
        help_text=_('Required. 254 characters or fewer.'
                    ' Letters, digits and @/./+/-/_ only.')
    )
    first_name = models.CharField(
        _('First Name'), max_length=30, blank=True, help_text=_('First name.')
    )
    last_name = models.CharField(
        _('Last Name'), max_length=30, blank=True, help_text=_('Last name.')
    )
    date_joined = models.DateTimeField(
        _('Member since'), auto_now_add=True
    )
    is_active = models.BooleanField(
        _('Active'), default=True
    )
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.')
    )
    points = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('last_name', 'first_name', 'email')
        unique_together = ('email', 'first_name')


class UserReferrerCode(models.Model):
    owner_user = models.ForeignKey('users.User',
                                   null=False,
                                   db_index=True,
                                   related_name='owner_referrer_code',
                                   on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, null=False, unique=False)
    referrer_user = models.ForeignKey('users.User',
                                      null=True,
                                      blank=True,
                                      related_name='referrer_code',
                                      on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name=_('created'),
                                      auto_now_add=True,
                                      null=True,
                                      blank=True)
    updated_at = models.DateTimeField(verbose_name=_('updated'),
                                      auto_now_add=False,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return f'Owner:{self.owner_user.email} code:{self.code}' \
               f' referrer user:' \
               f'{self.referrer_user and self.referrer_user.email}'

    class Meta:
        db_table = 'user_referrer_code'
        verbose_name = _('Referrer code')
        unique_together = ('owner_user', 'referrer_user')
