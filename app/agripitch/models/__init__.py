import itertools
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django import forms
from django.forms import modelform_factory

User = get_user_model()


def image_directory_path(instance, filename):
    return (f'agri_pitch_2022/{instance.application}/{filename}')


def competition_image_directory_path(instance, filename):
    return (f'competitions/{instance.slug}/{filename}')


class AFDBApplication(models.Model):

    applicant = models.OneToOneField(
        User,
        verbose_name=_('Applicant'),
        related_name=_('afdb_application'),
        on_delete=models.CASCADE)

    def __str__(self) -> str:
        return _('AFDB Application for ') + self.applicant.full_name

    class Meta:
        verbose_name_plural = _('AFDB Applications')


class Competition(models.Model):

    image = models.ImageField(
        upload_to=competition_image_directory_path,
        help_text=_('An image to display in the call to action page.'))
    tagline = models.CharField(
        max_length=255, help_text=_('A title for the call to action.'))
    description = models.TextField(
        help_text=_('A description of what the call to action is about.'))
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text=_('Unique text to append to the address for the call to action.'))
    deadline = models.DateTimeField(
        help_text=_('The call to action\'s deadline.'))
    created = models.DateTimeField(
        auto_now_add=True, help_text=_('The date the call to action was created.'))
    updated = models.DateTimeField(
        auto_now=True, help_text='The date the call to action was updated.')
    available_for_applications = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether applications can be made '
            'for this call to action. If checked it and is within the deadline, '
            'applicants can view it on the application page.'))

    def __str__(self):
        return self.tagline

    class Meta:
        verbose_name_plural = _('Competitions')

    def _generate_slug(self):
        value = self.tagline
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Competition.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)


class ShortList(models.Model):

    label = models.CharField(max_length=200)
    competition = models.ForeignKey(
        Competition,
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


class DynamicForm(forms.Form):

    def __init__(self, instance, *args, **kwargs):
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


def get_form(instance):
    return DynamicForm(instance)


class SubCriteriaItem(models.Model):

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

    @property
    def input(self):
        return get_form(self)

    def __str__(self) -> str:
        return self.label


class SubCriteriaItemChoice(models.Model):

    choice = models.CharField(max_length=200)
    sub_criteria_item = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='choices')

    def __str__(self) -> str:
        return self.choice


class SubCriteriaItemResponse(models.Model):

    application = models.ForeignKey(
        AFDBApplication, on_delete=models.CASCADE,
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
        AFDBApplication, on_delete=models.CASCADE, related_name='documents')


class SubCriteriaInputFieldPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_inputs')
    value = models.CharField(max_length=400)
    application = models.ForeignKey(
        AFDBApplication, on_delete=models.CASCADE, related_name='text_inputs')

    def __str__(self) -> str:
        return self.value


class SubCriteriaTextFieldInputPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_area_inputs')
    value = models.TextField(max_length=400)
    application = models.ForeignKey(
        AFDBApplication, on_delete=models.CASCADE,
        related_name='text_area_inputs')

    def __str__(self) -> str:
        return self.value
