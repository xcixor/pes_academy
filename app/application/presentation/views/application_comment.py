from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from application.models import ApplicationComment
from application.forms import ApplicationCommentForm


class ApplicationCommentView(FormView):

    template_name = 'eligibility/eligibility.html'
    form_class = ApplicationCommentForm
    model = ApplicationComment

    def form_valid(self, form):
        self.comment = form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _('Great, your comment has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.comment.application.slug}/'

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
