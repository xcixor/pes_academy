from django.contrib import messages
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _
from accounts.models import Coach


class Coaching(CreateView):

    model = Coach
    fields = ['coach', 'mentee']
    template_name = 'profile/coach_bio.html'

    def get_success_url(self) -> str:
        success_message = self.object.coach.full_name + \
            _(' Has been added as your coach.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/accounts/bio/{self.object.coach.pk}/'
