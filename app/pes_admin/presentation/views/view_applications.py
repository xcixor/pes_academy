from django.views.generic import ListView
from application.models import Application


class ApplicationsView(ListView):

    template_name = 'pes_admin/view_applications.html'
    model = Application
    context_object_name = 'applications'
