from django.views.generic import ListView
from application.models import Application


class ApplicationsView(ListView):

    template_name = 'pes_admin/view_applications.html'
    model = Application
    context_object_name = 'applications'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        self.request.session.pop('sort', None)
        self.request.session.pop('search', None)
        return super().get(request, *args, **kwargs)
