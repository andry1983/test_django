import logging
from datetime import datetime
from socket import gaierror

from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
    is_safe_url,
)
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (
    FormView, RedirectView, TemplateView,
    CreateView,
)

# pylint: disable=import-error,no-name-in-module
from apps.users.models import User, UserReferrerCode
from apps.users.decorators import anonymous_required
from apps.users.forms import (
    UserAuthenticationForm,
    UserCreateForm,
)
from apps.users.services.points.points import update_referrer_owners_points

logger = logging.getLogger(__name__)


@method_decorator(anonymous_required(redirect_to='users:home'),
                  name='dispatch')
class LoginView(FormView):
    """
    Provides the ability to login as a user with a email and password
    """
    success_url = reverse_lazy('users:login')
    form_class = UserAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.jinja2'
    request = None

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to,
                           allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegistrationView(FormView):
    form_class = UserCreateForm
    template_name = 'registration.jinja2'
    success_url = reverse_lazy('users:registration-activate')

    def _send_confirmation_email(self, user: User):
        try:
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.jinja2', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
        except gaierror as e:
            logger.error('Failed to connect to smtp'
                         ' server please check smtp configuration settings')
            raise e

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        referral_code = form.cleaned_data.get('referral_code')
        if referral_code:
            code = UserReferrerCode.objects.filter(code=referral_code).first()
            if code.referrer_user:
                UserReferrerCode.objects.create(
                    owner_user=code.owner_user,
                    code=code.code,
                    referrer_user=user,
                    updated_at=datetime.utcnow()
                )
            else:
                code.referrer_user = user
                code.updated_at = datetime.utcnow()
                code.save()
            update_referrer_owners_points(code.owner_user.id)
        self._send_confirmation_email(user)
        return super().form_valid(form)


class RegistrationActivatePage(TemplateView):
    template_name = 'registration-activate.jinja2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:home'))
        return super().get(request, *args, **kwargs)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class HomePage(TemplateView):
    template_name = 'home.jinja2'

    def get_context_data(self, **kwargs):
        referrer_data = UserReferrerCode.objects.filter(
            owner_user=self.request.user
        ).annotate(
            owner_email=F('owner_user__referrer_code__owner_user__email'),
            referrer_user_email=F('referrer_user__email'),
            referrer_user_name=F('referrer_user__first_name'),
        ).order_by('created_at', 'updated_at').all()
        return {
            'referrer_data': referrer_data
        }


class TopPage(TemplateView):
    template_name = 'top-10.jinja2'

    def get_context_data(self, **kwargs):
        top_users = User.objects.filter(
            points__gt=0
        ).order_by('-points')[:10]
        return {
            'top_users': top_users
        }


# pylint: disable=arguments-differ
class RegistrationSuccess(RedirectView):

    def dispatch(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404()
        else:
            valid_user = user and not user.is_active
            if valid_user and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                update_referrer_owners_points(user.id)
            if request.user.is_authenticated:
                self.url = 'users:home'
            else:
                self.url = 'users:login'

        return super().dispatch(request, uidb64, token, *args, **kwargs)

    def get_redirect_url(self, request, *args, **kwargs):
        return reverse_lazy(self.url)


# pylint: disable=attribute-defined-outside-init
@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ReferrerCodeCreateView(CreateView):
    http_method_names = ['post']
    model = UserReferrerCode
    template_name = 'home.jinja2'
    success_url = reverse_lazy('users:home')
    fields = ('code',)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = UserReferrerCode.objects.create(
                owner_user=self.request.user
            )
        return HttpResponseRedirect(self.get_success_url())
