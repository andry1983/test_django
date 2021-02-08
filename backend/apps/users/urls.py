from django.urls import re_path, path

from backend.apps.users.views import (
    LoginView,
    LogoutView,
    HomePage,
    RegistrationView,
    RegistrationSuccess, RegistrationActivatePage, ReferrerCodeCreateView,
    TopPage,
)

app_name = 'users'

urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^registration/$', RegistrationView.as_view(),
            name='registration'),
    re_path(r'^registration-activate/$', RegistrationActivatePage.as_view(),
            name='registration-activate'),
    path('registration-success/<uidb64>/<token>/',
         RegistrationSuccess.as_view(),
         name='registration-success'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path('^$', HomePage.as_view(), name='home'),
    re_path('top-10', TopPage.as_view(), name='top_10'),
    re_path('^referrer-code/create$', ReferrerCodeCreateView.as_view(),
            name='referrer-code-create'),
]
