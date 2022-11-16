from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from application.forms import ApplicationPromptForm
from eligibility.models import ShortListGroup


class ApplicationPromptView(FormView):

    form_class = ApplicationPromptForm
    template_name = 'eligibility/eligibility.html'

    def form_valid(self, form):
        self.prompt = form.save(self.request.user)
        form.send_prompt(
            self.prompt.application.application_creator.email, self.prompt.application.reviewers.first().reviewer.email, self.request)
        return super().form_valid(form)

    def get_success_url(self):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        success_message = _('Great, your prompt has been sent.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.prompt.application.slug}/{step.slug}/'

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
