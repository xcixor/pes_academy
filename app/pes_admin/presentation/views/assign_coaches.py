from django.views.generic import DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from pes_admin.forms import AssignCoachesForm

User = get_user_model()


class GetAssignCoaches(DetailView):

    template_name = 'pes_admin/assign_coaches.html'
    model = User
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AssignCoachesForm
        return context


class PostAssignCoaches(SingleObjectMixin, FormView):

    template_name = 'pes_admin/assign_coaches.html'
    form_class = AssignCoachesForm
    success_url = '/admin/advanced/users/call-to-action/'
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.is_in_review = True
        self.object.save()
        form.assign_coaches(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _('Great, user ') + \
            self.object.full_name + _(' now has coaches.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().get_success_url()


class AssignCoachesView(View):

    def get(self, request, *args, **kwargs):
        view = GetAssignCoaches.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostAssignCoaches.as_view()
        return view(request, *args, **kwargs)
