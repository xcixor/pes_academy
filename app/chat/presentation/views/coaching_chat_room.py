from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from accounts.models import Coach


class CoachingChatRoomView(LoginRequiredMixin, DetailView):

    model = Coach
    template_name = 'chat/coach_chat_room.html'
    context_object_name = 'coach'

    def get(self, request, *args, **kwargs):
        coach = self.get_object()
        current_user = self.request.user
        if coach in current_user.coaches.all():
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden()
