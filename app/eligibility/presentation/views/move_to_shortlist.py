from django.views.generic import DetailView, CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, View
from application.models import Application
from agripitch.models import PhaseTwoApplicationMarks
from accounts.models import User


class GetMoveToShortList(DetailView, FormMixin):

    template_name = 'eligibility/move_to_shortlist.html'
    model = Application
    context_object_name = 'application'

    def get_form(self, form_class=None):
        application = self.object
        data = {}
        for reviewer in application.reviewers.all():
            data['reviewer'] = reviewer
        PhaseTwoApplicationMarksFormSet = inlineformset_factory(
            Application, PhaseTwoApplicationMarks,
            fields=['reviewer', 'total_marks'],
            max_num=application.reviewers.count())
        # application_queryset = Application.objects.filter(pk=application.pk)
        # PhaseTwoApplicationMarksFormSet.form.base_fields['application'].queryset = application_queryset
        reviewer_queryset = application.reviewers.all()
        PhaseTwoApplicationMarksFormSet.form.base_fields['reviewer'].queryset = reviewer_queryset
        # PhaseTwoApplicationMarksFormSet.form.base_fields['application'].initial = application
        formset = PhaseTwoApplicationMarksFormSet(
            initial=[data], instance=application)
        return formset


class PostMoveToShortList(View, SingleObjectMixin):

    template_name = 'eligibility/move_to_shortlist.html'
    model = Application
    context_object_name = 'application'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        application = self.get_object()
        return HttpResponseRedirect(f'/eligibility/{application.slug}/shortlist/')

    # def form_invalid(self, form):
    #     print(form)
    #     return super().form_invalid(form)

    # def form_valid(self, form):
    #     # print(form, '********')
    #     return super().form_valid(form)

    # def get_form(self, form_class=None):
    #     application = self.object
        # data = {}
        # for reviewer in application.reviewers.all():
        #     data['reviewer'] = reviewer
        # PhaseTwoApplicationMarksFormSet = inlineformset_factory(
        #     Application, PhaseTwoApplicationMarks,
        #     fields=['reviewer', 'total_marks'],
        #     max_num=application.reviewers.count())
        # # application_queryset = Application.objects.filter(pk=application.pk)
        # # PhaseTwoApplicationMarksFormSet.form.base_fields['application'].queryset = application_queryset
        # reviewer_queryset = application.reviewers.all()
        # PhaseTwoApplicationMarksFormSet.form.base_fields['reviewer'].queryset = reviewer_queryset
        # # PhaseTwoApplicationMarksFormSet.form.base_fields['application'].initial = application
        # formset = PhaseTwoApplicationMarksFormSet(
        #     initial=[data], instance=application)
    #     return formset


class MoveToShortList(View):

    def get(self, request, *args, **kwargs):
        view = GetMoveToShortList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostMoveToShortList.as_view()
        return view(request, *args, **kwargs)


def move_application_to_shortlist(request, slug):
    application = Application.objects.get(slug=slug)
    data = {}
    for review in application.reviewers.all():
        data['reviewer'] = review.reviewer
    PhaseTwoApplicationMarksFormSet = inlineformset_factory(
        Application, PhaseTwoApplicationMarks,
        fields=['reviewer', 'total_marks'],
        max_num=application.reviewers.count())
    if request.method == "POST":
        formset = PhaseTwoApplicationMarksFormSet(
            request.POST, instance=application)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                f'/eligibility/{application.slug}/shortlist/')
        message = _(
            'Something went wrong, please check your form below.')
        print(formset.errors)
        messages.add_message(request, messages.ERROR, message)
        return render(
            request,
            'eligibility/move_to_shortlist.html',
            {'formset': formset})
    else:
        reviewer_ids = application.reviewers.all().values_list('pk', flat=True)
        reviewer_queryset = User.objects.filter(pk__in=reviewer_ids)
        PhaseTwoApplicationMarksFormSet.form.base_fields['reviewer'].queryset = reviewer_queryset
        formset = PhaseTwoApplicationMarksFormSet(
            initial=[data], instance=application)
    return render(
        request,
        'eligibility/move_to_shortlist.html',
        {'formset': formset})
