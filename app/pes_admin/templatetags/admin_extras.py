from django import template
from django_countries import countries
from application.models import Application
from agripitch.models import SubCriteriaItem, SubCriteriaItemResponse

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
