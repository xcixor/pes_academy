from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from staff.models import Event


class SessionsView(TemplateView):

    template_name = 'staff/sessions.html'


class GetSessionView(TemplateView):

    template_name = 'staff/session.html'


class PostSessionView(CreateView):

    template_name = 'staff/session.html'
    fields = ['coach', 'coachee', 'title', 'description']
    model = Event
    success_url = '/staff/sessions/'


class SessionView(View):

    def get(self, request, *args, **kwargs):
        view = GetSessionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSessionView.as_view()
        return view(request, *args, **kwargs)


class SessionDetails(DetailView):

    template_name = 'staff/session_details.html'
    model = Event
    context_object_name = 'session'


class SessionUpdate(UpdateView):

    template_name = 'staff/session_details.html'
    model = Event
    fields = ['description']

    def get_success_url(self) -> str:
        return f'/staff/session/{self.object.pk}/'
