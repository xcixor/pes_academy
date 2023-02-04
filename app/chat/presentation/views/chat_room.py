from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from academy.models import Session


class ChatRoomView(LoginRequiredMixin, DetailView):

    model = Session
    template_name = 'chat/room.html'
    context_object_name = 'session'

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        current_user = self.request.user
        if session in current_user.sessions.all() or session in current_user.events.all():
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden()
