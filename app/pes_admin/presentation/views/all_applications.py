from django.views.generic import ListView
from application.models import Application


class AllApplicationsView(ListView):

    template_name = 'pes_admin/all_applications.html'
    model = Application
    context_object_name = 'applications'
