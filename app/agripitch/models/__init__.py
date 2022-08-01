from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from application.models import CallToAction, Application
from django import forms

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


class CriteriaItem(models.Model):

    label = models.CharField(max_length=400)
    shortlist = models.ForeignKey(
        ShortList, on_delete=models.CASCADE,
        related_name='criteria')

    def __str__(self) -> str:
        return self.label


def get_sub_criteria_item_response_if_exist(sub_criteria_item):
    response = None
    try:
        response = SubCriteriaItemResponse.objects.get(
            sub_criteria_item=sub_criteria_item)
    except SubCriteriaItemResponse.DoesNotExist:
        pass
    return response


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


def get_form(instance):
    return DynamicForm(instance)


class SubCriteriaItem(models.Model):

    a = [1, 2, 3, 4]

    FIELD_CHOICES = [
        ('charfield', 'Charfield'),
        ('textfield', 'Textfield'),
        ('choicefield', 'ChoiceField'),
        ('file', 'FileField')
    ]

    label = models.CharField(max_length=400)
    criteria = models.ForeignKey(
        CriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria')
    type = models.CharField(max_length=100, choices=FIELD_CHOICES)
    position_in_form = models.CharField(
        max_length=3, default=0)

    @property
    def input(self):
        return get_form([self])

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ('position_in_form',)


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

    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='properties')
    name = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.value


class SubCriteriaItemChoice(models.Model):

    choice = models.CharField(max_length=200)
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='choices')

    def __str__(self) -> str:
        return self.choice


class SubCriteriaItemResponse(models.Model):

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='responses')
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='responses')
    value = models.TextField()


class SubCriteriaDocumentPrompt(models.Model):

    label = models.CharField(max_length=200)
    document = models.FileField(
        upload_to=image_directory_path)
    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_documents')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='application_documents')


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
