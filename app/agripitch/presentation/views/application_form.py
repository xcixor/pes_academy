from django.views.generic import DetailView
from agripitch.models import Competition


class ApplicationFormView(DetailView):

    template_name = 'agripitch/application_form.html'
    model = Competition
    context_object_name = 'competition'
