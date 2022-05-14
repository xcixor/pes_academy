from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from staff.models import Meeting, Session


class GetSetupMeetingPageView(DetailView):

    template_name = 'staff/meeting_setup.html'
    model = Session
    context_object_name: str = 'session'


class SetupMeetingView(CreateView):

    template_name = 'staff/meeting_setup.html'
    model = Meeting
    fields = ['session', 'link']

    def get_success_url(self) -> str:
        message = _(
            'Great! a meeting has been added to your event')
        messages.add_message(
            self.request, messages.SUCCESS, message)
        return f'/staff/session/{self.object.session.pk}/'

    def form_invalid(self, form):
        message = _(
            'Hmm! something went wrong, please try again.')
        messages.add_message(
            self.request, messages.ERROR, message)
        return super().form_invalid(form)
