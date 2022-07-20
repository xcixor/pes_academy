from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def image_directory_path(instance, filename):
    return (f'agri_pitch_2022/{instance.application}/{filename}')


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


class ShortList(models.Model):

    label = models.CharField(max_length=200)
    afdb_application = models.ForeignKey(
        AFDBApplication,
        on_delete=models.CASCADE,
        verbose_name=_("Application"))


class CriteriaItem(models.Model):

    label = models.CharField(max_length=400)
    shortlist = models.ForeignKey(
        ShortList, on_delete=models.CASCADE,
        related_name='criteria')


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
