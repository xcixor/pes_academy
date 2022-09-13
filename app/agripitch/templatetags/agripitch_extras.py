from django import template
from agripitch.models import DynamicForm

register = template.Library()


@register.filter('get_item_from_dict')
def get_item_from_dict(dictionary, key):
    return dictionary.get(key)


@register.filter('get_form')
def get_form(sub_criteria, application):
    return DynamicForm(application, [sub_criteria])


@register.filter('sort_by_position_in_form')
def sort_by_position_in_form(queryset):
    if queryset:
        return queryset.order_by('position_in_form')
    else:
        return queryset
