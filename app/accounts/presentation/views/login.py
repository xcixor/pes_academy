from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from common.utils.common_queries import get_application
from accounts.forms import LoginForm


class UserLoginView(LoginView):

    template_name = "registration/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            self.request.session.modified = True
        return super(UserLoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        success_message = _('Welcome back ') + self.request.user.username
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        user = self.request.user
        application, msg = get_application(user)
        if application:
            if application.stage == 'step_one':
                next_url = f'/agripitch/{application.call_to_action.slug}/application/'
                return next_url
        next_url = self.request.GET.get("next", None)
        if next_url:
            return next_url
        return settings.LOGIN_REDIRECT_URL
