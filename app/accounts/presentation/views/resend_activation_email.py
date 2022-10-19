from django.views.generic import FormView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.forms import ResendActivationEmail


class ResendActivationEmailView(FormView):

    template_name = 'registration/resend_activation_email.html'
    success_url = '/accounts/activation-email-sent/'
    form_class = ResendActivationEmail

    def form_valid(self, form):
        form.resend_account_activation_email(self.request)
        error_message = _(
            'We have sent you the activation email to your address')
        messages.add_message(
            self.request, messages.SUCCESS, error_message)
        return super().form_valid(form)
