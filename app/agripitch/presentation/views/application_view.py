from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from agripitch.models import CriteriaItem
from common.utils.common_queries import get_application
from application.models import Application


class ApplicationView(LoginRequiredMixin, DetailView):

    template_name = 'agripitch/application_view.html'
    context_object_name = 'application'
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        return context
