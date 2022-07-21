from django.views.generic import ListView
from django.utils import timezone
from agripitch.models import Competition


class IndexView(ListView):

    template_name = "index/index.html"
    model = Competition
    context_object_name = 'calls_to_action'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            available_for_applications=True,
            deadline__gte=timezone.now())
        return queryset
