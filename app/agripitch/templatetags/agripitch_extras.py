from django import template
from agripitch.models import DynamicForm

register = template.Library()


@register.filter('get_item_from_dict')
def get_item_from_dict(dictionary, key):
    return dictionary.get(key)


@register.filter('get_form')
def get_form(sub_criteria, application):
    return DynamicForm(application, [sub_criteria])
