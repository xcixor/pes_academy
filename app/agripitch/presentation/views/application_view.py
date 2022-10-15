from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from agripitch.models import CriteriaItem
from common.utils.common_queries import get_application
from application.models import Application


class ApplicationView(LoginRequiredMixin, TemplateView):

    template_name = 'agripitch/application_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        user = self.request.user
        application, msg = get_application(user)
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=self.get_object()
            )
        return context
