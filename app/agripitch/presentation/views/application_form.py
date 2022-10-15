import json
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from common.utils.common_queries import get_application
from application.models import CallToAction, Application
from agripitch.models import (
    SubCriteriaItemResponse, SubCriteriaItem, CriteriaItem,
    DynamicForm, SubCriteriaItemDocumentResponse,
    get_sub_criteria_item_response_if_exist)
from django.http import JsonResponse
from agripitch.utils import get_sub_criteria_item_by_label
from common.utils.email import HtmlEmailMixin


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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.available_for_applications or self.object.deadline < timezone.now():
            message = _(
                "Sorry, the AFDB Agripitch Competition 2022 is not yet live!")
            messages.add_message(
                request, messages.INFO, message)
            return redirect(reverse('agripitch:agripitch_landing_page'))
        context = self.get_context_data(object=self.object)
        if request.user.application.stage == 'step_one':
            return self.render_to_response(context)
        return redirect(reverse('agripitch:application_view'))


def process_inputs(inputs, application):
    for key, value in inputs.items():
        sub_criteria_item = get_sub_criteria_item_by_label(key)
        if sub_criteria_item.type == 'multiplechoicefield':
            SubCriteriaItemResponse.objects.update_or_create(
                application=application,
                sub_criteria_item=sub_criteria_item,
                defaults={
                    'list_value': value,
                    'value': "",
                }
            )
        else:
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
    error_messages = {}
    for key, value in files.items():
        sub_criteria_item = get_sub_criteria_item_by_label(key)
        property_labels = [
            item.name for item in sub_criteria_item.properties.all()]
        if 'max_size' in property_labels:
            validation = validate_file_max_size(value[0], sub_criteria_item)
            is_valid = validation['status']
            error_messages[key] = [
                {'message': validation['message'], 'code': validation['code']}]
    return is_valid, error_messages


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


def save_personal_info(application):
    user = application.application_creator
    for item in SubCriteriaItem.objects.all():
        if item.criteria.label == 'Personal Information':
            response = get_sub_criteria_item_response_if_exist(
                item, application)
            if item.label == 'Full Name *':
                user.full_name = response.value
                user.save()
            if item.label == 'Language *':
                user.preferred_language = response.value
                user.save()
            if item.label == 'Gender *':
                user.gender = response.value
                user.save()
            if item.label == 'Date of Birth *':
                dob = datetime.datetime.strptime(response.value, "%Y-%m-%d")
                today = datetime.date.today()
                age = today - dob.date()
                age = age.days / 365.25
                user.age = round(age)
                user.save()
    return user


class PostApplicationFormView(SingleObjectMixin, View, HtmlEmailMixin):

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
                request.user.application,
                [sub_criteria_item],
                request.POST, request.FILES)
        elif is_ajax and dict_files:
            form = DynamicForm(request.user.application, [], request.FILES)
        elif not is_ajax:
            form = DynamicForm(
                request.user.application,
                SubCriteriaItem.objects.all(),
                request.POST, request.FILES)

        valid_files = True
        error_messages = {}
        if dict_files:
            valid_files, error_messages = validate_files(dict_files)

        if not form.is_valid() or not valid_files:
            form_errors = json.loads(form.errors.as_json())
            form_errors.update(error_messages)
            context = {}
            context['form'] = form
            context['form_errors'] = form_errors
            context['criteria'] = CriteriaItem.objects.all()
            context['competition'] = self.object
            if is_ajax:
                return JsonResponse(
                    form_errors, status=400)
            error_message = (
                "Please correct the errors in your form.")
            messages.add_message(
                request, messages.ERROR, error_message)
            return render(request, self.template_name, context)
        process_inputs(data, request.user.application)
        process_files(dict_files, request.user.application)
        if is_ajax:
            return JsonResponse(
                data, status=201)
        success_message = (
            "Your application has been recorded, we will get back to you shortly")
        messages.add_message(
            request, messages.SUCCESS, success_message)
        application = request.user.application
        # application.stage = 'step_two'
        # application.save()
        updated_user = save_personal_info(application)
        print(updated_user.full_name, '**********')
        self.send_email(updated_user)
        return redirect(reverse('agripitch:application_view'))

    def send_email(self, user):
        subject = _(
            'African Development Bank AgriPitch Competition '
            '2022 Application')
        message = ""
        from_email = settings.VERIFIED_EMAIL_USER
        to_email = [user.email]
        message = ('Thanks for applying to the African Development Bank '
                   'AgriPitch Competition 2022. Your application has '
                   'been recorded, we will get back to you shortly')
        context = {
            'email_address': user.email,
            'name': user.full_name,
            'subject': subject,
            'message': message,
            'date': timezone.now()
        }
        return super().send_email(
            subject, None, from_email, to_email,
            template='email/agripitch/application_confirmation.html',
            context=context)


class ApplicationFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = GetApplicationFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostApplicationFormView.as_view()
        return view(request, *args, **kwargs)
