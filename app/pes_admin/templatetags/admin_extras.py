from django import template
from django.db.models import Avg, Count
from application.models import Application
from agripitch.models import SubCriteriaItem, SubCriteriaItemResponse

register = template.Library()


@register.filter('get_total_applications')
def get_total_applications(string_to_invoke_call):
    return Application.objects.count()


@register.filter('get_total_applications_by_country')
def get_total_applications_by_country(string_to_invoke_call):
    sub_criteria_item = SubCriteriaItem.objects.get(label='Country *')
    applications = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria_item).distinct('value')
    applications_by_country = []
    for application in applications:
        applications_by_country.append(
            {
                application.value: SubCriteriaItemResponse.objects.filter(
                    value=application.value).count()
            }
        )
    return applications_by_country


@register.filter('get_total_applications_by_entity_type')
def get_total_applications_by_entity_type(string_to_invoke_call):
    sub_criteria_item = SubCriteriaItem.objects.get(label='Entity type *')
    applications = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria_item).distinct('value')
    applications_by_country = []
    for application in applications:
        applications_by_country.append(
            {
                application.value: SubCriteriaItemResponse.objects.filter(
                    value=application.value).count()
            }
        )
    return applications_by_country

@register.filter('get_total_applications_by_language_speakers')
def get_total_applications_by_language_speakers(string_to_invoke_call):
    sub_criteria_item = SubCriteriaItem.objects.get(label='Language *')
    applications = SubCriteriaItemResponse.objects.filter(
        sub_criteria_item=sub_criteria_item).distinct('value')
    applications_by_country = []
    for application in applications:
        applications_by_country.append(
            {
                application.value: SubCriteriaItemResponse.objects.filter(
                    value=application.value).count()
            }
        )
    return applications_by_country
