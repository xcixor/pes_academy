from django import template
from django_countries import countries as dj_countries
from application.models import Application
from agripitch.models import (
    SubCriteriaItem, SubCriteriaItemResponse,
    CriteriaItem)
from accounts.models import User

register = template.Library()


@register.filter('get_total_applications')
def get_total_applications(string_to_invoke_call):
    return Application.objects.count()


@register.filter('get_total_applications_by_criteria')
def get_total_applications_by_criteria(criteria):
    sub_criteria_item = None
    try:
        sub_criteria_item = SubCriteriaItem.objects.get(label=criteria)
    except SubCriteriaItem.DoesNotExist as e:
        print(e)
    responses = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria_item, application__stage='step_two').distinct('value')
    applications_by_criteria = []
    for response in responses:
        title = response.value
        if criteria == 'Country *':
            title = dict(dj_countries)[title]
            applications_by_criteria.append(
                [title, SubCriteriaItemResponse.objects.filter(
                    value=response.value, application__stage='step_two').count()]
            )
        else:
            applications_by_criteria.append(
                [title, SubCriteriaItemResponse.objects.filter(
                    value=response.value, application__stage='step_two').count()]
            )
    return applications_by_criteria


@register.filter('get_applications_by_stage')
def get_applications_by_stage(string_to_invoke_call):
    applications_by_stage = []
    step_one_applications = Application.objects.filter(
        stage='step_one').count()
    step_two_applications = Application.objects.filter(
        stage='step_two').count()
    step_three_applications = Application.objects.filter(
        stage='step_three').count()
    step_four_applications = Application.objects.filter(
        stage='step_four').count()
    applications_by_stage = [
        ['Application Data Not Submitted', step_one_applications],
        ['Data Submitted', step_two_applications],
        ['Documents in review', step_three_applications],
        ['Verdict Passed', step_four_applications],
    ]
    return applications_by_stage


@register.filter('get_total_afdb_applicants')
def get_total_afdb_applicants(string_to_invoke_call):
    applicants = User.objects.filter(is_applying_for_a_call_to_action=True)
    return applicants


@register.filter('get_responses_by_step')
def get_responses_by_step(string_to_invoke_call):
    criteria = CriteriaItem.objects.all()
    applications_by_step = []
    for criterion in criteria:
        unique_response = 0
        form_questions_in_criterion = [
            form_question for form_question in criterion.sub_criteria.all()]
        responses = [form_question.responses.count()
                     for form_question in form_questions_in_criterion]
        if len(responses) > 0:
            unique_response = max(responses)
        applications_by_step.append([criterion, unique_response])
    return applications_by_step


@register.filter('get_total_applications_by_country')
def get_total_applications_by_country(string_to_invoke_call):
    applications = Application.objects.filter(stage='step_two')
    sub_criteria_item = None
    try:
        sub_criteria_item = SubCriteriaItem.objects.get(label='Country *')
    except SubCriteriaItem.DoesNotExist as e:
        print(e)
    countries = []
    for application in applications:
        country = SubCriteriaItemResponse.objects.get(
            application=application.pk, sub_criteria_item=sub_criteria_item.pk)
        countries.append(country)
    uniques = set(countries)
    uniques = uniques
    uniques_with_count = []
    for item in uniques:
        nums = countries.count(item)
        title = item.value
        uniques_with_count.append([dict(dj_countries)[title], nums])
    return uniques_with_count
