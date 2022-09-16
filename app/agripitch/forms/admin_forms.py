from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import Input
from agripitch.models import SubCriteriaItemFieldProperties


class Datalist(Input):
    input_type = 'text'
    template_name = 'forms/widgets/datalist.html'
    option_template_name = 'forms/widgets/datalist_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False


class DatalistField(forms.ChoiceField):
    widget = Datalist
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }

    def __init__(self, *, choices='', **kwargs):
        super().__init__(**kwargs)
        self.choices = choices


NAME_CHOICES = (
    ('class', 'class'),
    ('accept', 'accept'),
    ('max_size', 'max_size'),
    ('required', 'required'),
    ('min', 'min'),
    ('max', 'max')
)
VALUE_CHOICES = (
    ('form-input-validate', 'form-input-validate'),
    ('form-radio', 'form-radio'),
    ('form-input-validate form-radio', 'form-input-validate form-radio'),
    ('.pdf', 'PDF'),
    ('image/*', 'Images'),
    ('1048576', '1 MB'),
    ('2097152', '2 MB'),
    ('False', 'Not required'),
    ('1987-01-01', 'Min Year'),
    ('2004-01-01', 'Max Year'),
    ('form-input-validate form-radio multiple_checkbox',
     'form-input-validate form-radio multiple_checkbox')
)


class SubCriteriaItemFieldPropertiesAdminForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.Select(choices=NAME_CHOICES),
        required=True
    )
    value = forms.CharField(
        widget=forms.Select(choices=VALUE_CHOICES),
        required=True
    )

    class Meta:
        model = SubCriteriaItemFieldProperties
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubCriteriaItemFieldPropertiesAdminForm,
              self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['name'].widget = Input()
            self.fields['value'].widget = Input()
            self.fields['name'].value = self.instance.name
            self.fields['value'].value = self.instance.value
        else:
            self.fields['name'].widget.template_name = 'forms/widgets/datalist.html'
            self.fields['value'].widget.template_name = 'forms/widgets/datalist.html'
