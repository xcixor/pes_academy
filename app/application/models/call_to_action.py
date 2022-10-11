from django.db import models
from django.utils.translation import get_language
from ckeditor.fields import RichTextField
from translations.models import Translatable


def image_directory_path(instance, filename):
    return (f'applications/{instance.slug}/{filename}')


class CallToAction(Translatable):

    image = models.ImageField(
        upload_to=image_directory_path,
        help_text='An image to display in the call to action page.')
    tagline = models.CharField(
        max_length=255, help_text='A title for the call to action.')
    description = RichTextField(
        help_text='A description of what the call to action is about.')
    description_fr = RichTextField(
        help_text='A description of what the call to action is about.',
        blank=True, null=True)
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text='Unique text to append to the address for the call to action.')
    deadline = models.DateTimeField(
        help_text='The call to action\'s deadline.')
    created = models.DateTimeField(
        auto_now_add=True, help_text='The date the call to action was created.')
    updated = models.DateTimeField(
        auto_now=True, help_text='The date the call to action was updated.')
    available_for_applications = models.BooleanField(
        default=False, help_text='Designates whether applications can be made '
        'for this call to action. If checked it and is within the deadline, '
        'applicants can view it on the application page.')

    def __str__(self):
        return self.get_tagline

    @property
    def get_tagline(self):
        language = get_language()
        if language == 'fr':
            item = CallToAction.objects.filter(
                pk=self.pk).translate('fr')[0]
            return item.tagline
        return self.tagline

    @property
    def get_description(self):
        language = get_language()
        if language == 'fr' and self.description_fr:
            return self.description_fr
        return self.description_fr

    class Meta:
        verbose_name_plural = 'Calls to Action'

    class TranslatableMeta:
        fields = ['tagline']
