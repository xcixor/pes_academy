from django.db import models
from ckeditor.fields import RichTextField


def image_directory_path(instance, filename):
    return (f'carousel/{filename}')


class CarouselImage(models.Model):

    caption = RichTextField()
    image = models.FileField(
        upload_to=image_directory_path)

    def __str__(self) -> str:
        return self.caption
