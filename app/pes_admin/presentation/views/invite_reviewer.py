from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from pes_admin.forms import InviteSubscriberForm


class GetInviteReviewerView(TemplateView):

    template_name = 'pes_admin/invite_reviewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InviteSubscriberForm
        return context


class PostInviteReviewerView(FormView):

    template_name = 'pes_admin/invite_reviewer.html'
    success_url = '/admin/advanced/'
    form_class = InviteSubscriberForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        form.send_invitation_email(self.request)
        success_message = _('Great. ') + email + \
            _(' has been asked to create an account.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = _(
            'Hmm..That didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)


class InviteReviewerView(View):

    def get(self, request, *args, **kwargs):
        view = GetInviteReviewerView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostInviteReviewerView.as_view()
        return view(request, *args, **kwargs)
