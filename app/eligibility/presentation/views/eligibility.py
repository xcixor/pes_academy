from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView


class EligibilityView(PermissionRequiredMixin, TemplateView):

    template_name = 'eligibility/eligibility.html'
    permission_required = ('application.view_application', )
