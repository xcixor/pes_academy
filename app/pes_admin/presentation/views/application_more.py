from django.views.generic import DetailView, UpdateView, View
from application.models import Application, ApplicationDraftData


class GetApplicationDetails(DetailView):

    template_name = 'pes_admin/application_details.html'
    context_object_name = 'application'
    model = Application


class AdvanceAvoidApplicationView(UpdateView):

    template_name = 'pes_admin/application_details.html'
    model = Application
    fields = ['to_advance', 'stage']

    def get_success_url(self) -> str:
        return f'/admin/advanced/view/{self.object.slug}/'


class ApplicationDetails(View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationDetails.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AdvanceAvoidApplicationView.as_view()
        return view(request, *args, **kwargs)
