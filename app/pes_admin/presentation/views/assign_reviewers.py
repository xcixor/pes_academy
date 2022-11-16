from django.views.generic import DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from application.models import Application
from pes_admin.forms import AssignReviewersForm


class GetAssignReviewers(DetailView):

    template_name = 'pes_admin/assign_reviewers.html'
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AssignReviewersForm
        return context


class PostAssignReviewers(SingleObjectMixin, FormView):

    template_name = 'pes_admin/assign_reviewers.html'
    form_class = AssignReviewersForm
    success_url = '/CgDX4znLdQDLFw/advanced/applications/unassigned/'
    model = Application

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.is_in_review = True
        self.object.stage = 'step_three'
        self.object.save()
        form.assign_reviewers(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _('Great, application ') + \
            str(self.object) + _(' is now in review.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()


class AssignReviewersView(View):

    def get(self, request, *args, **kwargs):
        view = GetAssignReviewers.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostAssignReviewers.as_view()
        return view(request, *args, **kwargs)
