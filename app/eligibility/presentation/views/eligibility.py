from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from application.models import Application


User = get_user_model()


class EligibilityView(PermissionRequiredMixin, DetailView):

    template_name = 'eligibility/eligibility.html'
    permission_required = ('application.can_view_application', )
    permission_denied_message = (
        'Hmm it seems that you cannot view this application '
        'please contact your admin.')
    model = Application
    context_object_name = 'application'
