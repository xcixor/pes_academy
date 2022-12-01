from django.contrib import messages
from django.views.generic import FormView, DeleteView
from django.utils.translation import gettext_lazy as _
from application.models import ApplicationComment
from application.forms import ApplicationCommentForm
from eligibility.models import ShortListGroup


class StepApplicationCommentView(FormView):

    template_name = 'eligibility/step.html'
    form_class = ApplicationCommentForm
    model = ApplicationComment

    def form_valid(self, form):
        self.comment = form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        success_message = _('Great, your comment has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.comment.application.slug}/{step.slug}/'

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)


class DeleteStepComment(DeleteView):

    model = ApplicationComment
    template_name = 'eligibility/step.html'

    def get_success_url(self):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        success_message = _('Great, your comment has been deleted.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.application.slug}/{step.slug}/'

    def delete(self, request, *args, **kwargs):
        self.application = self.get_object().application
        return super().delete(request, *args, **kwargs)

    def form_invalid(self, form):
        error_message = _('Hmm, that didn\'t work please try again.')
        messages.add_message(
            self.request, messages.ERROR, error_message)
        return super().form_invalid(form)
