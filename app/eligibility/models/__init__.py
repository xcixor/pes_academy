import itertools
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models
from agripitch.models import SubCriteriaItem
from application.models import Application


class ShortListGroup(models.Model):

    GROUPS = (
        ('step_one', _('Eligibility Verification')),
        ('step_two', _('Document Verification')),
        ('step_three', _('Long List')),
        ('step_four', _('Short List')),
    )

    group = models.CharField(
        verbose_name=_('Group'),
        choices=GROUPS,
        default='step_one',
        max_length=100
    )
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text=_('Unique text to append to the address for the application.'))

    def _generate_slug(self):
        value = self.get_group_display()
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not ShortListGroup.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_group_display()

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
        verbose_name_plural = "1. Short List Group Items"


class BonusPoints(models.Model):

    bonus = models.IntegerField()
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='bonus')
    step = models.OneToOneField(
        ShortListGroup, on_delete=models.SET_NULL,
        related_name='bonus', null=True)

    class Meta:
        verbose_name_plural = "2. Bonus"
