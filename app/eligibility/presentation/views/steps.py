from django.views.generic import DetailView
from eligibility.models import ShortListGroup
from application.models import Application
from django.utils.translation import gettext_lazy as _


class EvaluationStepView(DetailView):

    template_name = 'eligibility/step.html'
    partial_template_name = 'eligibility/partial/step.html'
    permission_required = ('application.can_view_application', )
    permission_denied_message = _(
        'Hmm it seems that you cannot view this application '
        'please contact your admin.')
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        context = super().get_context_data(**kwargs)
        context.update({'criteria': step})
        return context

    def get_template_names(self):
        if self.request.htmx:
            return self.partial_template_name
        return self.template_name
