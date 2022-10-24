from django.views.generic import TemplateView
from application.models import Application


class AllApplicationsView(TemplateView):

    template_name = 'pes_admin/all_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.all()
        return context
