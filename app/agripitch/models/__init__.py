from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from application.models import CallToAction, Application
from django.shortcuts import get_object_or_404


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

    def __init__(self, instance, *args, **kwargs):
        response = get_sub_criteria_item_response_if_exist(instance)
        super(DynamicForm, self).__init__(*args, **kwargs)
        if instance.type == 'charfield':
            self.fields[instance.label] = forms.CharField(max_length=400)
        elif instance.type == 'textfield':
            self.fields[instance.label] = forms.CharField(
                widget=forms.Textarea)
        elif instance.type == 'choicefield':
            initial_choices = [
                (choice.choice, choice.choice)
                for choice in instance.choices.all()]
            self.fields[instance.label] = forms.ChoiceField()
            self.fields[instance.label].choices = initial_choices
        elif instance.type == 'file':
            self.fields[instance.label] = forms.FileField()
        if not instance.type == 'file' and response:
            self.initial[instance.label] = response.value


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
        max_length=3, unique=True)

    @property
    def input(self):
        return get_form(self)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ('position_in_form',)


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
