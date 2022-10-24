from django.views.generic import DetailView
from agripitch.models import CriteriaItem
from application.models import Application


class AdminApplicationView(DetailView):

    template_name = 'agripitch/application_view.html'
    context_object_name = 'application'
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        return context
