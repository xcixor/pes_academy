from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from staff.models import Session


class SessionsView(TemplateView):

    template_name = 'staff/sessions.html'


class GetSessionView(TemplateView):

    template_name = 'staff/session.html'


class PostSessionView(CreateView):

    template_name = 'staff/session.html'
    fields = ['coach', 'coachee', 'title', 'description']
    model = Session
    success_url = '/staff/sessions/'


class SessionView(View):

    def get(self, request, *args, **kwargs):
        view = GetSessionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSessionView.as_view()
        return view(request, *args, **kwargs)
