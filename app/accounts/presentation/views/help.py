from django.views.generic import FormView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.forms import HelpForm


class HelpView(FormView):

    template_name = "help.html"
    form_class = HelpForm
    success_url = '/accounts/help/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        success_message = _('Thank you, your message has been received. We\'ll get back to you shortly.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()
