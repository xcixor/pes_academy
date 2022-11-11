from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _
from application.models import Application
from agripitch.models import CriteriaItem


User = get_user_model()


class EligibilityView(PermissionRequiredMixin, DetailView):

    template_name = 'eligibility/eligibility.html'
    partial_template_name = 'eligibility/partial/eligibility.html'
    permission_required = ('application.can_view_application', )
    permission_denied_message = _(
        'Hmm it seems that you cannot view this application '
        'please contact your admin.')
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        return context

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name
