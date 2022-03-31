from django.views.generic import ListView
from application.models import Application


class InReviewApplicationsView(ListView):

    template_name = 'pes_admin/in_review_applications.html'
    model = Application
    context_object_name = 'applications'

    def get_queryset(self):
        return super().get_queryset().filter(is_in_review=True)
