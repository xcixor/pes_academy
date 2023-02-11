from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import Coach
from academy.models import Session
from common.utils.email import HtmlEmailMixin


User = get_user_model()


class Coaching(CreateView, HtmlEmailMixin):

    model = Coach
    fields = ['coach', 'mentee']
    template_name = 'coach/coach_bio.html'

    def get_success_url(self) -> str:
        success_message = str(self.object.coach) + \
            _(' Has been added as your coach.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        to_email = self.object.coach.email
        from_email = settings.VERIFIED_EMAIL_USER
        message_piece_one = _("Hi, ")
        message_piece_two = _(" has added you as their coach.")
        email_message = message_piece_one + \
            str(self.object.mentee) + message_piece_two
        subject = _('PSA Student')
        context = {
            'message': email_message,
        }
        super().send_email(
            subject, None, from_email, [to_email],
            template='coach/email/new_student.html', context=context)
        return f'/accounts/bio/{self.object.coach.pk}/'


class CoachSessions(TemplateView):

    template_name = 'coach/coach_session.html'
    context_object_name = 'coach'

    def get_context_data(self, **kwargs):
        coach = User.objects.get(pk=kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['coach'] = coach
        return context


class SessionView(DetailView):

    template_name = 'coach/session.html'
    model = Session
    context_object_name = 'session'
