from django.views.generic import DetailView
from application.models import Application


class ApplicationDetails(DetailView):

    template_name = 'pes_admin/application_details.html'
    context_object_name = 'application'
    model = Application
