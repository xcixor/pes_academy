from django.views.generic import DetailView, UpdateView
from application.models import Application, ApplicationReview
from django.contrib.auth import get_user_model
from pes_admin.forms import (
    AssignReviewersForm)

User = get_user_model()


class ReassignApplicationHomeView(DetailView):

    template_name = 'pes_admin/reassign.html'
    model = Application
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        reviewers = User.objects.filter(is_reviewer=True)
        context = super().get_context_data(**kwargs)
        context['reviewers'] = reviewers
        context['form'] = AssignReviewersForm

        return context


class ReassignApplicationView(UpdateView):

    template_name = 'pes_admin/reassign.html'
    fields = ['reviewer']
    model = ApplicationReview

    def get_success_url(self) -> str:
        return '/CgDX4znLdQDLFw/advanced/applications/in-review/'
