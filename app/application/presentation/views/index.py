from django.views.generic import ListView
from django.utils import timezone
from application.models import CallToAction


class IndexView(ListView):

    template_name = "index/index.html"
    model = CallToAction
    context_object_name = 'calls_to_action'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            available_for_applications=True,
            deadline__gte=timezone.now())
        return queryset
