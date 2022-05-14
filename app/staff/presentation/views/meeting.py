from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from staff.models import Meeting, Session
from common.utils.email import HtmlEmailMixin


class GetSetupMeetingPageView(DetailView):

    template_name = 'staff/meeting_setup.html'
    model = Session
    context_object_name: str = 'session'


class SetupMeetingView(CreateView, HtmlEmailMixin):

    template_name = 'staff/meeting_setup.html'
    model = Meeting
    fields = ['session', 'link']

    def post(self, request, *args, **kwargs):
        self.session = Session.objects.get(pk=kwargs['pk'])
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        success_message = _(
            'Great! a meeting has been added to your event')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        to_email = self.object.session.coachee.email
        from_email = settings.VERIFIED_EMAIL_USER
        email_message = _(
            'Hi, your coach has set up a new meeting.'
            'Please click the link to book and select your availability, '
            'thank you.'
        )
        subject = 'Event Booking'
        context = {
            'message': email_message,
            'link': self.object.link
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='staff/email/event.html', context=context)
        return f'/staff/session/{self.object.session.pk}/'

    def form_invalid(self, form):
        message = _(
            'Hmm! something went wrong, please try again.')
        messages.add_message(
            self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        context['session'] = self.session
        return self.render_to_response(context)
