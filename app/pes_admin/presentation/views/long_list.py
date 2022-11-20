from django.views.generic import ListView
from application.models import Application, ApplicationEvaluator


class LongListEvaluation(ListView):

    model = Application
    template_name = 'pes_admin/long_list.html'
    context_object_name = 'applications'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().filter(stage='step_five')
        unassigned_applications = []
        applications_in_evaluation = ApplicationEvaluator.objects.all(
        ).values_list('application__id', flat=True)
        for application in queryset:
            if application.id not in applications_in_evaluation:
                unassigned_applications.append(application)
        return unassigned_applications
