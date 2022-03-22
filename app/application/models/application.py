import itertools
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from application.models.call_to_action import CallToAction


User = get_user_model()


class Application(models.Model):

    STAGE_CHOICES = (
        ('step_one', 'Application Data Not Submitted'),
        ('step_two', 'Data Submitted'),
        ('step_three', 'Documents in review'),
        ('step_four', 'Verdict Passed')
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    application_creator = models.OneToOneField(
        User, related_name='application', on_delete=models.CASCADE)
    call_to_action = models.ForeignKey(
        CallToAction, related_name='applications',
        on_delete=models.SET_NULL,
        null=True)
    stage = models.CharField(
        choices=STAGE_CHOICES,
        default='step_one',
        max_length=100
    )
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text='Unique text to append to the address for the application.')
    is_in_review = models.BooleanField(default=False)
    eligibility = models.BooleanField(default=False)
    to_advance = models.BooleanField(
        default=False, help_text='Whether to advance or avoid the application')
    milestones = models.TextField()
    expected_max_score = models.IntegerField(default=0)

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
        filled_id = f'{self.id}'.zfill(3)
        return f'PES - {self.slug} - {filled_id}'

    @property
    def total_score(self):
        return sum(item.score for item in self.scores.all())

    def __str__(self) -> str:
        return f'{self.call_to_action} - {self.application_creator}'
