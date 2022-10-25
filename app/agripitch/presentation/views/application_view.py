from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from agripitch.models import CriteriaItem
from django.template.loader import render_to_string
from application.models import Application


class ApplicationView(LoginRequiredMixin, DetailView):

    template_name = 'agripitch/application_view.html'
    context_object_name = 'application'
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        if self.object.application_creator == user:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        context = {}
        content = render_to_string(
            '404.html',
            context,
            request
        )
        return HttpResponseNotFound(content)
