from django.utils.translation import gettext_lazy as _
from django.db import models
from agripitch.models import SubCriteriaItem


class ShortListGroup(models.Model):

    GROUPS = (
        ('step_one', _('Application Data Not Submitted')),
    )

    group = models.CharField(
        verbose_name=_('Group'),
        choices=GROUPS,
        default='step_one',
        max_length=100
    )

    class Meta:
        verbose_name_plural = "1. Short List Group"


class ShortListGroupItems(models.Model):

    group = models.ForeignKey(
        ShortListGroup, on_delete=models.CASCADE,
        related_name='questions')
    question = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE,
        related_name='groups')

    class Meta:
        verbose_name_plural = "2. Short List Group Items"
