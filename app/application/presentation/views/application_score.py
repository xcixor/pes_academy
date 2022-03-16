from django.contrib import messages
from django.views.generic import CreateView
from application.models import ApplicationScore


class ApplicationScore(CreateView):

    template_name = 'eligibility/eligibility.html'
    fields = ['score', 'prompt', 'application']
    model = ApplicationScore

    def form_valid(self, form):
        self.score = form.save()
        self.score.reviewer = self.request.user
        self.score.save()
        return super().form_valid(form)

    def get_success_url(self):
        success_message = (
            'Great, your score has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.score.application.slug}/'

    def form_invalid(self, form):
        print(form.errors)
        error_message = (
            'Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
