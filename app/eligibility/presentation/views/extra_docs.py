from django.views.generic import DetailView
from application.models import Application


class ExtraDocumentsView(DetailView):

    template_name = "eligibility/extra_docs.html"
    model = Application
    context_object_name = 'application'
