from django import forms
from django.forms.widgets import Input
from agripitch.models import SubCriteriaItemFieldProperties


NAME_CHOICES = (
    ('class', 'Class'),
    ('accept', 'Files to Accept'),
    ('max_size', 'Max Size'),
    ('required', 'Required'),
    ('min', 'Min'),
    ('max', 'Max'),
    ('maxwords', 'Max Words')
)
VALUE_CHOICES = (
    ('form-input-validate', 'Class to validate inputs'),
    ('form-radio', 'form-radio'),
    ('form-input-validate form-radio', 'Classes to validate radio inputs'),
    ('.pdf', 'PDF'),
    ('image/*', 'Images'),
    ('1048576', '1 MB'),
    ('2097152', '2 MB'),
    ('False', 'Not required'),
    ('1987-01-01', 'Min Year'),
    ('2004-01-01', 'Max Year'),
    ('form-input-validate form-radio multiple_checkbox',
     'Classes to validate multiple checkbox inputs')
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
