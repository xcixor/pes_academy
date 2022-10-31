from django.views.generic import ListView
from application.models import Application


class InReviewApplicationsView(ListView):

    template_name = 'pes_admin/in_review_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(stage='step_three')
