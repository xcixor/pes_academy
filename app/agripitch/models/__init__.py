import itertools
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

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
        related_name='short_lists',
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


class SubCriteriaItem(models.Model):

    label = models.CharField(max_length=400)
    criteria = models.ForeignKey(
        ShortList, on_delete=models.CASCADE,
        related_name='sub_criteria')


class SubCriteriaDocumentPrompt(models.Model):

    label = models.CharField(max_length=200)
    document = models.FileField(
        upload_to=image_directory_path)
    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_documents')


class SubCriteriaInputFieldPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_inputs')
    value = models.CharField(max_length=400)


class SubCriteriaTextFieldInputPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_text_area_inputs')
    value = models.CharField(max_length=400)


class SubCriteriaSelectFieldInputPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_select_inputs')


class SubCriteriaSelectFieldInputPromptChoice(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='select_choices')
    value = models.CharField(max_length=400)


class SubCriteriaRadioFieldInputPrompt(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='sub_criteria_radio_inputs')


class SubCriteriaRadioFieldInputPromptOption(models.Model):

    sub_criteria = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='radio_options')
    value = models.CharField(max_length=400)
