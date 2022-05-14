from django.views.generic import TemplateView


class SetupMeetingView(TemplateView):

    template_name = 'staff/meeting_setup.html'
