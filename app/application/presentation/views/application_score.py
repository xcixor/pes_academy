from django.contrib import messages
from django.views.generic import FormView
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from application.forms import ApplicationScoreForm
from django.views.generic.detail import SingleObjectMixin
from application.models import Application


class ApplicationScoreView(SingleObjectMixin, FormView):

    template_name = 'eligibility/eligibility.html'
    form_class = ApplicationScoreForm
    model = Application

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.score = form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _('Great, your score has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.score.application.slug}/'

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return redirect(f'/eligibility/{self.object.slug}/')
