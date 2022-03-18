from django.contrib import messages
from django.views.generic import FormView
from application.forms import ApplicationScoreForm


class ApplicationScoreView(FormView):

    template_name = 'eligibility/eligibility.html'
    form_class = ApplicationScoreForm

    def form_valid(self, form):
        self.score = form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = (
            'Great, your score has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.score.application.slug}/'

    def form_invalid(self, form):
        error_message = (
            'Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
