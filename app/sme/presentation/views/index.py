from django.views.generic import ListView
from sme.models import Application


class IndexView(ListView):

    template_name = "index/index.html"
    model = Application
    context_object_name = 'applications'
