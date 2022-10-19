from django import template
from django_countries import countries
from application.models import Application
from agripitch.models import SubCriteriaItem, SubCriteriaItemResponse
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
    applications = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria_item).distinct('value')
    applications_by_criteria = []
    for application in applications:
        title = application.value
        if criteria == 'Country *':
            title = dict(countries)[title]
        applications_by_criteria.append(
            [title, SubCriteriaItemResponse.objects.filter(
                value=application.value).count()]
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
