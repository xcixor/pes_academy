from django import forms
from agripitch.utils import get_sub_criteria_item_response_if_exist


class DynamicForm(forms.Form):

    def __init__(self, sub_criteria_items, *args, **kwargs):
        super(DynamicForm, self).__init__(*args, **kwargs)
        for instance in sub_criteria_items:
            properties = {}
            for validator in instance.validators.all():
                properties[validator.validator.name] = validator.value
            response = get_sub_criteria_item_response_if_exist(instance)
            if instance.type == 'charfield':
                self.fields[instance.label] = forms.CharField(**properties)
            elif instance.type == 'textfield':
                self.fields[instance.label] = forms.CharField(
                    **properties,
                    widget=forms.Textarea)
            elif instance.type == 'choicefield':
                initial_choices = [
                    (choice.choice, choice.choice)
                    for choice in instance.choices.all()]
                self.fields[instance.label] = forms.ChoiceField(**properties)
                self.fields[instance.label].choices = initial_choices
            elif instance.type == 'file':
                self.fields[instance.label] = forms.FileField(**properties)
            if not instance.type == 'file' and response:
                self.initial[instance.label] = response.value
            for property in instance.properties.all():
                self.fields[instance.label].widget.attrs[property.name] = property.value
