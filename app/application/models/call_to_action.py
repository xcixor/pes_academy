from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def image_directory_path(instance, filename):
    return (f'applications/{instance.slug}/{filename}')


class CallToAction(models.Model):

    image = models.ImageField(
        upload_to=image_directory_path,
        help_text='An image to display in the call to action page.')
    tagline = models.CharField(
        max_length=255, help_text='A title for the call to action.')
    description = models.TextField(
        help_text='A description of what the call to action is about.')
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
        return self.tagline

    class Meta:
        verbose_name_plural = 'Calls to Action'
