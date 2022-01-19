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
