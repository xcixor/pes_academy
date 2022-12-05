from django.views.generic import ListView
from application.models import Application


class LongListEvaluation(ListView):

    model = Application
    template_name = 'pes_admin/long_list.html'
    context_object_name = 'applications'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().filter(stage='step_five')
        sorted_queryset = sorted(
            queryset.all(), key=lambda t: t.average_marks, reverse=True)
        return sorted_queryset
