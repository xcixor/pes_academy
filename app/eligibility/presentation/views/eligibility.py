from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

User = get_user_model()


class EligibilityView(PermissionRequiredMixin, TemplateView):

    template_name = 'eligibility/eligibility.html'
    permission_required = ('application.can_view_application', )
    permission_denied_message = (
        'Hmm it seems that you cannot view this application '
        'please contact your admin.')
