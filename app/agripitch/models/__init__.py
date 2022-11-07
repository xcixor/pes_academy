from django.db import models
from django.forms import Select
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.utils.translation import get_language
from ckeditor.fields import RichTextField
from translations.models import Translatable
from django_countries.fields import CountryField
from application.models import CallToAction, Application


User = get_user_model()


def image_directory_path(instance, filename):
    return (f'agri_pitch_2022/{instance.application}/{filename}')


def competition_image_directory_path(instance, filename):
    return (f'competitions/{instance.slug}/{filename}')


class ShortList(Translatable):

    label = models.CharField(max_length=200)
    competition = models.ForeignKey(
        CallToAction,
        related_name='shortlists',
        on_delete=models.CASCADE,
        verbose_name=_("Application"))

    def __str__(self) -> str:
        return self.get_label

    @property
    def get_label(self):
        language = get_language()
        if language == 'fr':
            item = ShortList.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.label
        return self.label

    class TranslatableMeta:
        fields = ['label']

    class Meta:
        verbose_name_plural = "1. Shortlists"


class CriteriaItem(Translatable):

    label = models.CharField(max_length=400)
    shortlist = models.ForeignKey(
        ShortList, on_delete=models.CASCADE,
        related_name='criteria')
    position_in_form = models.IntegerField(default=1)

    @property
    def get_label(self):
        language = get_language()
        if language == 'fr':
            item = CriteriaItem.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.label
        return self.label

    class TranslatableMeta:
        fields = ['label']

    def __str__(self) -> str:
        return self.get_label

    class Meta:
        verbose_name_plural = "2. Criteria Items"
        ordering = ['position_in_form']


def get_sub_criteria_item_response_if_exist(sub_criteria_item, application):
    response = None
    try:
        response = SubCriteriaItemResponse.objects.get(
            sub_criteria_item=sub_criteria_item, application=application)
    except SubCriteriaItemResponse.DoesNotExist:
        response = None
    return response


def get_multiplechoice_responses_if_exist(sub_criteria_item, application):
    response = None
    try:
        response = SubCriteriaItemResponse.objects.filter(
            sub_criteria_item=sub_criteria_item, application=application).values_list('list_value')
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


class CustomSelect(Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = True

        return option


class DynamicForm(forms.Form):

    def __init__(self, application, sub_criteria_items, *args, **kwargs):
        super(DynamicForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        response = None
        for instance in sub_criteria_items:
            properties = {}
            for validator in instance.validators.all():
                properties[validator.validator.name] = validator.value
            if instance.type == 'charfield':
                self.fields[instance.label] = forms.CharField(**properties)
            if instance.type == 'countryfield':
                self.fields[instance.label] = CountryField().formfield()
            if instance.type == 'datefield':
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
                    (choice.choice, choice)
                    for choice in instance.choices.all()]
                initial_choices.insert(0, ('', 'Select Option'))
                self.fields[instance.label] = forms.ChoiceField(
                    **properties, widget=CustomSelect)
                self.fields[instance.label].choices = initial_choices
            elif instance.type == 'multiplechoicefield':
                choices = [
                    (choice.choice, choice)
                    for choice in instance.choices.all()]
                self.fields[instance.label] = forms.MultipleChoiceField(
                    widget=forms.CheckboxSelectMultiple,
                    **properties)
                self.fields[instance.label].choices = choices

                responses = get_multiplechoice_responses_if_exist(
                    instance, application)
                initial_choices = []
                if responses:
                    for response in responses[0]:
                        if response:
                            for item in response:
                                initial_choices.append(item)
                    self.fields[instance.label].initial = initial_choices
            elif instance.type == 'radiofield':
                choices = [
                    (choice.choice, choice)
                    for choice in instance.choices.all()]
                self.fields[instance.label] = forms.CharField(
                    **properties, widget=forms.RadioSelect(choices=choices))
            elif instance.type == 'file':
                self.fields[instance.label] = forms.FileField(**properties)

            if instance.type == 'file':
                response = get_sub_criteria_item_document_response_if_exist(
                    instance, application)
                if response:
                    self.initial[instance.label] = response.document
            elif instance.type != 'file' and instance.type != 'multiplechoicefield':
                response = get_sub_criteria_item_response_if_exist(
                    instance, application)
                if response:
                    self.initial[instance.label] = response.value

            for property in instance.properties.all():
                if property.name == 'required' and property.value == 'False':
                    self.fields[instance.label].required = False
                else:
                    self.fields[instance.label].widget.attrs[property.name] = property.value
            inputs_class = {'class': 'form-input'}
            if "class" not in self.fields[instance.label].widget.attrs.keys():
                self.fields[instance.label].widget.attrs.update(
                    inputs_class)
            else:
                self.fields[instance.label].widget.attrs['class'] += " form-input"
            if response:
                if "class" in self.fields[instance.label].widget.attrs.keys():
                    new_classes = self.fields[instance.label].widget.attrs['class'].replace(
                        "is-dependent", "")
                    self.fields[instance.label].widget.attrs.update(
                        {'class': new_classes.lstrip()})

                if instance.type == 'file':
                    if "class" in self.fields[instance.label].widget.attrs:
                        updated_class_value = self.fields[instance.label].widget.attrs['class'].replace(
                            "form-input-validate", "")
                        self.fields[instance.label].widget.attrs['class'] = updated_class_value.lstrip(
                        )
            language = get_language()

            self.fields[instance.label].widget.attrs['data-label-text'] = instance.label
            if language == 'fr':
                item = SubCriteriaItem.objects.filter(
                    pk=instance.pk).translate('fr')[0]
                self.fields[instance.label].label = item.label
                self.fields[instance.label].widget.attrs['data-label-text'] = item.label


def get_form(instance):
    return DynamicForm(instance)


class SubCriteriaItem(Translatable):

    FIELD_CHOICES = [
        ('charfield', 'One Line Text'),
        ('textfield', 'Multiple Line Text'),
        ('choicefield', 'Dropdown'),
        ('file', 'File'),
        ('numberfield', 'Number'),
        ('radiofield', 'Choice'),
        ('datefield', 'Date'),
        ('countryfield', 'Country'),
        ('multiplechoicefield', 'Multiple Choice Field')
    ]

    label = models.CharField(max_length=600)
    criteria = models.ForeignKey(
        CriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria')
    type = models.CharField(max_length=100, choices=FIELD_CHOICES)
    position_in_form = models.IntegerField(default=1)
    description = RichTextField(null=True, blank=True)
    description_fr = RichTextField(null=True, blank=True)

    def __str__(self) -> str:
        language = get_language()
        if language == 'fr':
            item = SubCriteriaItem.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.label
        return self.label

    class TranslatableMeta:
        fields = ['label']

    class Meta:
        ordering = ['position_in_form']
        verbose_name_plural = "3. Form Questions"

    @property
    def get_description(self):
        language = get_language()
        if language == 'fr' and self.description_fr:
            return self.description_fr
        return self.description


class Scale(Translatable):

    label = models.CharField(max_length=500)

    class TranslatableMeta:
        fields = ['label']

    class Meta:
        verbose_name_plural = "8. Scales"

    def __str__(self) -> str:
        language = get_language()
        if language == 'fr':
            item = Scale.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.label
        return self.label


class ScaleItem(Translatable):

    label = models.CharField(max_length=500)
    score = models.IntegerField()
    scale = models.ForeignKey(
        Scale, on_delete=models.SET_NULL,
        related_name='items', null=True)

    class TranslatableMeta:
        fields = ['label']

    class Meta:
        verbose_name_plural = "9. Scale Items"

    def __str__(self) -> str:
        language = get_language()
        if language == 'fr':
            item = ScaleItem.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.label
        return self.label


class Scoring(models.Model):

    question = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='scoring', null=True)
    scale = models.ForeignKey(
        Scale, on_delete=models.CASCADE,
        related_name='scoring', null=True)
    score = models.IntegerField()

    class Meta:
        verbose_name_plural = "10. Scoring"

    def __str__(self) -> str:
        return str(self.question)


class SubCriteriaItemFieldProperties(models.Model):

    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='properties')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.value


class SubCriteriaItemChoice(Translatable):

    choice = models.CharField(max_length=200)
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='choices')

    class TranslatableMeta:
        fields = ['choice']

    def __str__(self) -> str:
        language = get_language()
        if language == 'fr':
            item = SubCriteriaItemChoice.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.choice
        return self.choice

    class Meta:
        verbose_name_plural = '7 Choices'


class SubCriteriaItemResponse(models.Model):

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='responses')
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='responses')
    value = models.TextField(blank=True, null=True)
    list_value = ArrayField(
        ArrayField(
            models.CharField(max_length=400, blank=True, null=True),
        ),
        blank=True, null=True
    )

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


def partner_logo_directory_path(instance, filename):
    return (f'carousel/{filename}')


class PartnerLogo(models.Model):

    title = models.CharField(max_length=400, unique=True)
    image = models.FileField(
        upload_to=partner_logo_directory_path)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    for_footer = models.BooleanField(default=False)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.title} Logo'

    class Meta:
        ordering = ['position']
        verbose_name_plural = '6 Partner Logos'
