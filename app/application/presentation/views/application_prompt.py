from django.contrib import messages
from django.views.generic import FormView
from application.forms import ApplicationPromptForm


class ApplicationPromptView(FormView):

    form_class = ApplicationPromptForm
    template_name = 'eligibility/eligibility.html'

    def form_valid(self, form):
        self.prompt = form.save(self.request.user)
        form.send_prompt(
            self.prompt.application.application_creator.email, self.request)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = (
            'Great, your prompt has been sent.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.prompt.application.slug}/'

    def form_invalid(self, form):
        error_message = (
            'Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
