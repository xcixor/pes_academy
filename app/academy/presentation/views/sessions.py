from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView)
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from academy.models import Session


class SessionsView(TemplateView):

    template_name = 'staff/sessions.html'


class GetSessionView(TemplateView):

    template_name = 'staff/session.html'


class PostSessionView(CreateView):

    template_name = 'staff/session.html'
    fields = ['coach', 'coachee', 'title', 'description']
    model = Session

    def get_success_url(self) -> str:
        return reverse('academy:sessions')


class SessionView(View):

    def get(self, request, *args, **kwargs):
        view = GetSessionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSessionView.as_view()
        return view(request, *args, **kwargs)


class SessionDetails(DetailView):

    template_name = 'staff/session_details.html'
    model = Session
    context_object_name = 'session'


class SessionUpdate(UpdateView):

    template_name = 'staff/session_details.html'
    model = Session
    fields = ['title', 'description']

    def get_success_url(self) -> str:
        return reverse('academy:session_details', kwargs={'pk': self.object.pk})


class DeleteSessionView(DeleteView):

    model = Session
    template_name = 'staff/session_details.html'

    def get_success_url(self):
        success_message = _('Great, the session has been deleted.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return reverse('academy:sessions')

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
