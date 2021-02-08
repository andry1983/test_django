from django.contrib import admin

# pylint: disable=import-error,no-name-in-module
from apps.users.models import User, UserReferrerCode
from core import settings

if settings.DJANGO_ADMIN:
    admin.site.register(User)
    admin.site.register(UserReferrerCode)
