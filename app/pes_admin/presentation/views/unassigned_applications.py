from django.views.generic import ListView
from application.models import Application


class UnassignedApplicationsView(ListView):

    template_name = 'pes_admin/unassigned_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(is_in_review=False)
