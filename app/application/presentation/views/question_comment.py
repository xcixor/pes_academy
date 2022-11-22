from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django import forms
from application.models import QuestionComment


class QuestionCommentView(CreateView):

    model = QuestionComment
    template_name = 'eligibility/eligibility.html'
    fields = '__all__'

    def get_success_url(self) -> str:
        message = _('Great your comment has been saved!.')
        messages.add_message(self.request, messages.SUCCESS, message)
        slug = self.kwargs.get('slug')
        return f'/eligibility/{slug}/'

    def form_invalid(self, form):
        message = _(
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        application_slug = self.kwargs.get('slug')
        return redirect(f'/eligibility/{application_slug}/')
