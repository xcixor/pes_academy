from django.views.generic import ListView, TemplateView
from application.models import CallToAction


class IndexView(ListView):

    template_name = "index/index.html"
    model = CallToAction
    context_object_name = 'calls_to_action'
