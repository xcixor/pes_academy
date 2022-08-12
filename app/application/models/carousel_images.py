from django.db import models


def image_directory_path(instance, filename):
    return (f'carousel/{filename}')


class CarouselImage(models.Model):

    caption = models.CharField(max_length=200)
    image = models.FileField(
        upload_to=image_directory_path)

    def __str__(self) -> str:
        return self.caption
