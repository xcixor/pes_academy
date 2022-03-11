from django.db import models
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.utils.common_queries import get_application
from application.models import ApplicationDocument



class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "profile/dashboard.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application, msg = get_application(self.request.user)
        context['application'] = application
        return context


class ExtraDocumentView(CreateView):
    model = ApplicationDocument