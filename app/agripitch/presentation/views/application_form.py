import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse
from common.utils.common_queries import get_application
from application.models import CallToAction, Application
from agripitch.models import (
    SubCriteriaItemResponse, SubCriteriaItem, CriteriaItem)
from agripitch.utils import get_sub_criteria_item_by_label
from agripitch.models import DynamicForm


def get_application_form(sub_criteria_items):

    return DynamicForm(sub_criteria_items)


class GetApplicationFormView(DetailView):

    template_name = 'agripitch/application_form.html'
    model = CallToAction
    context_object_name = 'competition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'criteria': CriteriaItem.objects.all()})
        user = self.request.user
        application, msg = get_application(user)
        if not application:
            Application.objects.create(
                application_creator=user,
                call_to_action=self.get_object()
            )
        return context


def process_inputs(inputs, application):
    inputs.pop('csrfmiddlewaretoken')
    for key, value in inputs.items():
        if value[0] and not value[0].isspace():
            sub_criteria_item = get_sub_criteria_item_by_label(key)
            SubCriteriaItemResponse.objects.update_or_create(
                application=application,
                sub_criteria_item=sub_criteria_item,
                defaults={
                    'value': value[0]
                }
            )


def process_files(files, application):
    pass


class PostApplicationFormView(SingleObjectMixin, View):

    template_name = 'agripitch/application_form.html'
    model = CallToAction
    context_object_name = 'competition'
    form_class = DynamicForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DynamicForm(SubCriteriaItem.objects.all(), request.POST)
        if not form.is_valid():
            form_errors = json.loads(form.errors.as_json())
            context = {}
            context['form'] = form
            context['form_errors'] = form_errors
            context['criteria'] = CriteriaItem.objects.all()
            return render(request, self.template_name, context)
        return redirect(
            reverse(
                'agripitch:application',
                kwargs={'slug': self.object.slug}))


class ApplicationFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationFormView.as_view()
        return view(request, *args, **kwargs)
