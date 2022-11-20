from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django import forms
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from agripitch.models import ApplicationMarks, Application
from eligibility.models import ShortListGroup


class ScoringForm(forms.ModelForm):

    class Meta:
        model = ApplicationMarks
        fields = ['question', 'score', 'scoring']


class ScoreView(CreateView):

    model = ApplicationMarks
    template_name = 'eligibility/step.html'
    fields = ['application', 'question', 'score', 'scoring']

    def get_success_url(self):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        success_message = _('Great, your score has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        if step.group == 'step_three':
            return f'/eligibility/{self.object.application.slug}/'
        return f'/eligibility/{self.object.application.slug}/{step.slug}/'

    def form_invalid(self, form):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        message = _(
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        application = Application.objects.get(pk=self.kwargs.get('pk'))
        if step.group == 'step_three':
            return f'/eligibility/{application.slug}/'
        return redirect(f'/eligibility/{application.slug}/{step.slug}/')


class UpdateScoreView(SingleObjectMixin, FormView):

    model = Application
    template_name = 'eligibility/step.html'
    partial_template_name = 'eligibility/partial/step.html'
    form_class = ScoringForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        score = form.cleaned_data['score']
        scoring = form.cleaned_data['scoring']
        question = form.cleaned_data['question']
        marks = ApplicationMarks.objects.get(
            question=question, application=self.object, scoring=scoring)
        marks.score = score
        marks.save()
        return super().form_valid(form)

    def get_success_url(self):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        success_message = _('Great, your score has been updated.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        if step.group == 'step_three':
            return f'/eligibility/{self.object.slug}/'
        return f'/eligibility/{self.object.slug}/{step.slug}/'

    def form_invalid(self, form):
        step = ShortListGroup.objects.get(slug=self.kwargs.get('step_slug'))
        message = _(
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        if step.group == 'step_three':
            return f'/eligibility/{self.object.slug}/'
        return redirect(f'/eligibility/{self.object.slug}/{step.slug}/')
