from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django import forms
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from agripitch.models import ApplicationMarks, Application, Scoring


class ScoringForm(forms.ModelForm):

    class Meta:
        model = ApplicationMarks
        fields = ['scoring', 'score']


class ScoreView(CreateView):

    model = ApplicationMarks
    template_name = 'eligibility/eligibility.html'
    fields = ['application', 'scoring', 'score']

    def get_success_url(self):
        success_message = _('Great, your score has been saved.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.object.application.slug}/'

    def form_invalid(self, form):
        message = _(
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        application = Application.objects.get(pk=self.kwargs.get('pk'))
        return redirect(f'/eligibility/{application.slug}/')


class UpdateScoreView(SingleObjectMixin, FormView):

    model = Application
    template_name = 'eligibility/eligibility.html'
    form_class = ScoringForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        score = form.cleaned_data['score']
        scoring = form.cleaned_data['scoring']
        marks = ApplicationMarks.objects.get(
            scoring=scoring, application=self.object)
        marks.score = score
        marks.save()
        return super().form_valid(form)

    def get_success_url(self):
        success_message = _('Great, your score has been updated.')
        messages.add_message(
            self.request, messages.SUCCESS, success_message)
        return f'/eligibility/{self.object.slug}/'

    def form_invalid(self, form):
        message = _(
            'Something went wrong, please check your form below.')
        messages.add_message(self.request, messages.ERROR, message)
        context = self.get_context_data()
        context['form'] = form
        # application = Application.objects.get(pk=self.kwargs.get('pk'))
        return redirect(f'/eligibility/{self.object.slug}/')