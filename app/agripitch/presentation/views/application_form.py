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
    SubCriteriaItemResponse, SubCriteriaItem, CriteriaItem,
    DynamicForm, SubCriteriaItemDocumentResponse)
from django.http import JsonResponse
from agripitch.utils import get_sub_criteria_item_by_label


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
    for key, value in files.items():
        sub_criteria_item = get_sub_criteria_item_by_label(key)
        SubCriteriaItemDocumentResponse.objects.update_or_create(
            application=application,
            sub_criteria_item=sub_criteria_item,
            defaults={
                'name': key,
                'document': value[0]
            }
        )


def validate_files(files):
    is_valid = True
    messages = {}
    for key, value in files.items():
        sub_criteria_item = get_sub_criteria_item_by_label(key)
        property_labels = [
            item.name for item in sub_criteria_item.properties.all()]
        if 'max_size' in property_labels:
            validation = validate_file_max_size(value[0], sub_criteria_item)
            is_valid = validation['status']
            messages[key] = [
                {'message': validation['message'], 'code': validation['code']}]
    return is_valid, messages


def validate_file_max_size(file, sub_criteria_item):
    is_valid = True
    file_size = file.size
    max_size_in_kb = int(
        sub_criteria_item.properties.all().get(name='max_size').value)
    if file_size > max_size_in_kb:
        is_valid = False
    if not is_valid:
        max_size = max_size_in_kb / 1048576
        return {
            'status': is_valid,
            'message': f"{sub_criteria_item.label} is too big, maximum size should be {max_size}MB!",
            'code': 'max_size'}
    return {'status': is_valid, 'message': "Valid size", 'code': 'max_size'}


class PostApplicationFormView(SingleObjectMixin, View):

    template_name = 'agripitch/application_form.html'
    model = CallToAction
    context_object_name = 'competition'
    form_class = DynamicForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken', None)
        dict_files = dict(request.FILES)

        is_ajax = request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax and data:
            # assumption: ajax requests only post one item per request
            first_value = next(iter(data.keys()))
            sub_criteria_item = get_sub_criteria_item_by_label(first_value)
            form = DynamicForm(
                [sub_criteria_item],
                request.POST, request.FILES)
        elif is_ajax and dict_files:
            form = DynamicForm([], request.FILES)
        elif not is_ajax:
            form = DynamicForm(
                SubCriteriaItem.objects.all(),
                request.POST, request.FILES)

        valid_files = True
        messages = {}
        if dict_files:
            valid_files, messages = validate_files(dict_files)

        if not form.is_valid() or not valid_files:
            form_errors = json.loads(form.errors.as_json())
            form_errors.update(messages)
            context = {}
            context['form'] = form
            context['form_errors'] = form_errors
            context['criteria'] = CriteriaItem.objects.all()
            if is_ajax:
                return JsonResponse(
                    form_errors, status=400)
            return render(request, self.template_name, context)
        process_inputs(data, request.user.application)
        process_files(dict_files, request.user.application)
        if is_ajax:
            return JsonResponse(
                data, status=201)
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