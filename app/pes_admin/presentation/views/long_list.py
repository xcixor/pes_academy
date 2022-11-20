from itertools import chain
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from application.models import Application, ApplicationReview


class LongListEvaluation(ListView):

    model = Application
    template_name = 'pes_admin/long_list.html'
    context_object_name = 'applications'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().filter(stage='step_five')
        return queryset
