from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import Coach
from staff.models import Session
from common.utils.email import HtmlEmailMixin


User = get_user_model()


class Coaching(CreateView, HtmlEmailMixin):

    model = Coach
    fields = ['coach', 'mentee']
    template_name = 'coach/coach_bio.html'

    def get_success_url(self) -> str:
        success_message = self.object.coach.full_name + \
            _(' Has been added as your coach.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        to_email = self.object.coach.email
        from_email = settings.VERIFIED_EMAIL_USER
        email_message = _(
            f'Hi, {self.object.mentee.full_name} has added you as their coach.'
        )
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
