from django.views.generic import DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from application.models import Application
from application.models import ApplicationEvaluator

User = get_user_model()


class GetAssignEvaluator(DetailView):

    template_name = 'pes_admin/assign_evaluator.html'
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evaluators'] = User.objects.filter(
            is_staff=True, is_evaluator=True, is_reviewer=True)
        return context


# class PostAssignEvaluator(SingleObjectMixin, FormView):

#     template_name = 'pes_admin/assign_evaluator.html'
#     form_class = AssignEvaluatorForm
#     success_url = '/CgDX4znLdQDLFw/advanced/applications/unassigned/'
#     model = Application

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         self.object.is_in_review = True
#         self.object.stage = 'step_three'
#         self.object.save()
#         form.assign_evaluator(self.object)
#         return super().form_valid(form)

#     def get_success_url(self):
#         success_message = _('Great, application ') + \
#             str(self.object) + _(' is now in review.')
#         messages.add_message(
#             self.request, messages.SUCCESS, success_message)
#         return super().get_success_url()


class AssignEvaluatorView(View):

    def get(self, request, *args, **kwargs):
        view = GetAssignEvaluator.as_view()
        return view(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     view = PostAssignEvaluator.as_view()
    #     return view(request, *args, **kwargs)
