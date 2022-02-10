from django.db import models


def image_directory_path(instance, filename):
    return (f'applications/{instance.slug}/{filename}')


class Application(models.Model):

    image = models.ImageField(
        upload_to=image_directory_path,
        help_text='An image to display in the applications page.')
    tagline = models.CharField(
        max_length=255, help_text='A title for the application.')
    description = models.TextField(
        help_text='A description of what the application is about.')
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text='Unique text to append to the address for the application.')
    deadline = models.DateTimeField(help_text='The application\'s deadline.')
    created = models.DateTimeField(
        auto_now_add=True, help_text='The date the application was created.')
    updated = models.DateTimeField(
        auto_now=True, help_text='The date the application was updated.')
    available_for_applications = models.BooleanField(
        default=False, help_text='Designates whether applications can be made '
        'for this application. If checked it and is within the deadline, '
        'applicants can view it on the application page.')

    def __str__(self):
        return self.tagline
