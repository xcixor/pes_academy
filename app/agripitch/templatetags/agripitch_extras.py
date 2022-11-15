from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django import template
from agripitch.models import (
    DynamicForm, get_sub_criteria_item_document_response_if_exist,
    get_sub_criteria_item_response_if_exist, ApplicationMarks)
from agripitch.presentation.views import get_sub_criteria_item_by_label

register = template.Library()


@register.filter('get_item_from_dict')
def get_item_from_dict(dictionary, key):
    return dictionary.get(key)


@register.filter('get_form')
def get_form(sub_criteria, application):
    return DynamicForm(application, [sub_criteria])


@register.filter('get_response')
def get_response(sub_criteria, application):
    sub_criteria_item = get_sub_criteria_item_by_label(sub_criteria)
    if sub_criteria_item is not None:
        if sub_criteria_item.type == 'file':
            return get_sub_criteria_item_document_response_if_exist(
                sub_criteria_item, application)
        item = get_sub_criteria_item_response_if_exist(
            sub_criteria_item, application)
        if item:
            if sub_criteria_item.type == 'multiplechoicefield':
                str_response = ""
                for response in item.list_value:
                    str_response += response + ", "
                return str_response
            if item:
                return item.value
        return item
    return ""


@register.filter('get_marks')
def get_marks(application):
    total = 0
    for mark in application.marks.all():
        total += mark.score
    return total


@register.filter('get_age')
def get_age(response):
    today = date.today()
    dob = datetime.strptime(response, '%Y-%m-%d')
    age = relativedelta(today, dob)
    return f'{age.years} years and {age.months} months'


@register.filter('get_scoring_for_sub_criteria')
def get_scoring_for_sub_criteria(application, sub_criteria):
    existing_marks = ApplicationMarks.objects.filter(application=application)
    for mark in existing_marks:
        for scoring in mark.scoring.saved_scores.all():
            if scoring.scoring.question.pk == sub_criteria.pk:
                return True
            return False


@register.filter('is_scored')
def is_scored(scoring, application):
    found_marks = ApplicationMarks.objects.filter(
        scoring=scoring, application=application).first()
    if found_marks:
        return found_marks
    return False
