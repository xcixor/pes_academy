from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from accounts.models import Coach


User = get_user_model()


class Coaching(CreateView):

    model = Coach
    fields = ['coach', 'mentee']
    template_name = 'coach/coach_bio.html'

    def get_success_url(self) -> str:
        success_message = self.object.coach.full_name + \
            _(' Has been added as your coach.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/accounts/bio/{self.object.coach.pk}/'


class CoachSessions(TemplateView):

    template_name = 'coach/coach_session.html'
    context_object_name = 'coach'

    def get_context_data(self, **kwargs):
        coach = User.objects.get(pk=kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['coach'] = coach
        return context
