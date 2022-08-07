from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from application.models import CallToAction, Application


User = get_user_model()


def image_directory_path(instance, filename):
    return (f'agri_pitch_2022/{instance.application}/{filename}')


def competition_image_directory_path(instance, filename):
    return (f'competitions/{instance.slug}/{filename}')


class ShortList(models.Model):

    label = models.CharField(max_length=200)
    competition = models.ForeignKey(
        CallToAction,
        related_name='shortlists',
        on_delete=models.CASCADE,
        verbose_name=_("Application"))

    def __str__(self) -> str:
        return self.label

    class Meta:
        verbose_name_plural = "1. Shortlists"


class CriteriaItem(models.Model):

    label = models.CharField(max_length=400)
    shortlist = models.ForeignKey(
        ShortList, on_delete=models.CASCADE,
        related_name='criteria')

    def __str__(self) -> str:
        return self.label

    class Meta:
        verbose_name_plural = "2. Criteria Items"


def get_sub_criteria_item_response_if_exist(sub_criteria_item, application):
    response = None
    try:
        response = SubCriteriaItemResponse.objects.get(
            sub_criteria_item=sub_criteria_item, application=application)
    except SubCriteriaItemResponse.DoesNotExist:
        response = None
    return response


def get_sub_criteria_item_document_response_if_exist(sub_criteria_item, application):
    response = None
    try:
        response = SubCriteriaItemDocumentResponse.objects.get(
            sub_criteria_item=sub_criteria_item,
            application=application)
    except SubCriteriaItemDocumentResponse.DoesNotExist:
        response = None
    return response


class DynamicForm(forms.Form):

    def __init__(self, application, sub_criteria_items, *args, **kwargs):
        super(DynamicForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        for instance in sub_criteria_items:
            properties = {}
            for validator in instance.validators.all():
                properties[validator.validator.name] = validator.value
            if instance.type == 'charfield':
                self.fields[instance.label] = forms.CharField(**properties)
            if instance.type == 'countryfield':
                self.fields[instance.label] = CountryField().formfield()
            if instance.type == 'datefield':
                print('a date here')
                self.fields[instance.label] = forms.DateField(
                    widget=forms.DateInput(attrs={'type': 'date'}),
                    **properties)
            if instance.type == 'numberfield':
                self.fields[instance.label] = forms.IntegerField(**properties)
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
            elif instance.type == 'radiofield':
                choices = [
                    (choice.choice, choice.choice)
                    for choice in instance.choices.all()]
                self.fields[instance.label] = forms.CharField(
                    **properties, widget=forms.RadioSelect(choices=choices))
            elif instance.type == 'file':
                self.fields[instance.label] = forms.FileField(**properties)

            for property in instance.properties.all():
                if property.name == 'required' and property.value == 'False':
                    self.fields[instance.label].required = False
                else:
                    self.fields[instance.label].widget.attrs[property.name] = property.value
            if instance.type == 'file':
                response = get_sub_criteria_item_document_response_if_exist(
                    instance, application)
                if response:
                    self.initial[instance.label] = response.document
                    if "class" in self.fields[instance.label].widget.attrs:
                        updated_class_value = self.fields[instance.label].widget.attrs['class'].replace(
                            "form-input-validate", "")
                        self.fields[instance.label].widget.attrs['class'] = updated_class_value.lstrip(
                        )
            elif instance.type != 'file':
                response = get_sub_criteria_item_response_if_exist(
                    instance, application)
                if response:
                    self.initial[instance.label] = response.value
            inputs_class = {'class': 'form-input'}
            if "class" not in self.fields[instance.label].widget.attrs.keys():
                self.fields[instance.label].widget.attrs.update(inputs_class)
            else:
                self.fields[instance.label].widget.attrs['class'] += " form-input"


def get_form(instance):
    return DynamicForm(instance)


class SubCriteriaItem(models.Model):

    a = [1, 2, 3, 4]

    FIELD_CHOICES = [
        ('charfield', 'CharInput'),
        ('textfield', 'TextInput'),
        ('choicefield', 'ChoiceInput'),
        ('file', 'FileInput'),
        ('numberfield', 'NumberInput'),
        ('radiofield', 'RadioInput'),
        ('datefield', 'DateField'),
        ('countryfield', 'CountryField')
    ]

    label = models.CharField(max_length=600)
    criteria = models.ForeignKey(
        CriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria')
    type = models.CharField(max_length=100, choices=FIELD_CHOICES)
    position_in_form = models.CharField(
        max_length=3, default=0)
    description = RichTextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ('position_in_form',)
        verbose_name_plural = "3. Form Questions"


class ValidatorType(models.Model):

    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name


class SubCriteriaItemValidators(models.Model):

    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='validators')
    validator = models.ForeignKey(
        ValidatorType, on_delete=models.CASCADE,
        related_name='items')
    value = models.CharField(max_length=80)

    class Meta:
        unique_together = ('sub_criteria_item', 'validator')

    def __str__(self) -> str:
        return str(self.validator) + " : " + str(self.sub_criteria_item)


class SubCriteriaItemFieldProperties(models.Model):

    NAME_CHOICES = (
        ('class', 'class'),
        ('accept', 'accept'),
        ('max_size', 'max_size'),
        ('required', 'required')
    )
    VALUE_CHOICES = (
        ('form-input-validate', 'form-input-validate'),
        ('form-radio', 'form-radio'),
        ('form-input-validate form-radio', 'form-input-validate form-radio'),
        ('.pdf', 'PDF'),
        ('image/*', 'Images'),
        ('1048576', '1 MB'),
        ('2097152', '2 MB'),
        ('False', 'Not required')
    )

    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='properties')
    name = models.CharField(max_length=100, choices=NAME_CHOICES)
    value = models.CharField(max_length=400, choices=VALUE_CHOICES)

    def __str__(self) -> str:
        return self.value


class SubCriteriaItemChoice(models.Model):

    choice = models.CharField(max_length=200)
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='choices')
    description = RichTextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.choice


class SubCriteriaItemResponse(models.Model):

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='responses')
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='responses')
    value = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.value

    class Meta:
        unique_together = [['sub_criteria_item', 'application']]
        verbose_name_plural = '4 Responses'


class SubCriteriaItemDocumentResponse(models.Model):

    name = models.CharField(max_length=200)
    document = models.FileField(
        upload_to=image_directory_path)
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_item_documents')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='application_documents')

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = [['sub_criteria_item', 'application']]
        verbose_name_plural = '5 Documents'


class SubCriteriaInputFieldPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_inputs')
    value = models.CharField(max_length=400)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='text_inputs')

    def __str__(self) -> str:
        return self.value


class SubCriteriaTextFieldInputPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_area_inputs')
    value = models.TextField(max_length=400)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='text_area_inputs')

    def __str__(self) -> str:
        return self.value
