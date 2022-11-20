from django.views.generic import DetailView, CreateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from application.models import ApplicationEvaluator, Application

User = get_user_model()


class AssignEvaluatorView(DetailView):

    template_name = 'pes_admin/assign_evaluator.html'
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evaluators'] = User.objects.filter(
            is_staff=True, is_evaluator=True, is_reviewer=True)
        return context


class CreateEvaluation(CreateView):

    template_name = 'pes_admin/assign_evaluator.html'
    fields = ['application', 'evaluator']
    success_url = '/CgDX4znLdQDLFw/advanced/applications/long/list/evaluation/'
    model = ApplicationEvaluator

    def get_success_url(self):
        success_message = _('Great, application ') + \
            str(self.object) + _(' is now in evaluation.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()
