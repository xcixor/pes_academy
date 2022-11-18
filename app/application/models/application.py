import itertools
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from application.models.call_to_action import CallToAction


User = get_user_model()


class Application(models.Model):

    STAGE_CHOICES = (
        ('step_one', _('Application Data Not Submitted')),
        ('step_two', _('Data Submitted')),
        ('step_three', _('Eligibility Verification')),
        ('step_four', _('Document Verification')),
        ('step_five', _('Long List')),
        ('step_six', _('Short List')),
        ('step_seven', _('Verdict Passed')),
    )

    created = models.DateTimeField(
        verbose_name=_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name=_("Date Updated"), auto_now=True)
    application_creator = models.OneToOneField(
        User,
        verbose_name=_('Application Creator'),
        related_name=_('application'), on_delete=models.CASCADE)
    call_to_action = models.ForeignKey(
        CallToAction,
        verbose_name=_('Call To Action'),
        related_name=_('applications'),
        on_delete=models.SET_NULL,
        null=True)
    stage = models.CharField(
        verbose_name=_('Stage'),
        choices=STAGE_CHOICES,
        default='step_one',
        max_length=100
    )
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text=_('Unique text to append to the address for the application.'))
    is_in_review = models.BooleanField(
        verbose_name=_('In Review'), default=False)
    eligibility = models.BooleanField(
        verbose_name=_('Eligibility'), default=False)
    to_advance = models.BooleanField(
        verbose_name=_('Whether to Advance'),
        default=False,
        help_text=_('Whether to advance or avoid the application'))
    disqualified = models.BooleanField(
        verbose_name=_('Whether disqualified'),
        default=False,
        help_text=_('Whether application is disqualified'))

    def _generate_slug(self):
        value = self.call_to_action.tagline
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Application.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    @property
    def special_id(self):
        filled_id = f'{self.application_creator.id}'.zfill(3)
        return f'PES - {self.slug} - {filled_id}'

    @property
    def total_score(self):
        print('lol')
        return sum(item.score for item in self.marks.all())

    @property
    def total_bonus(self):
        return sum(item.bonus for item in self.bonus.all())

    @property
    def overall_score(self):
        return self.total_bonus + self.total_score

    def __str__(self) -> str:
        return f'{self.call_to_action} - {self.application_creator}'

    class Meta:
        ordering = ['application_creator__id']
