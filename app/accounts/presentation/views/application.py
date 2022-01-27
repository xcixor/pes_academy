from django.views.generic import DetailView
from sme.models import Application


class ApplicationView(DetailView):

    template_name = "application_form.html"
    model = Application
    context_object_name = 'application'
