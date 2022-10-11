from django.db import models
from django.utils.translation import get_language
from ckeditor.fields import RichTextField


def image_directory_path(instance, filename):
    return (f'carousel/{filename}')


class CarouselImage(models.Model):

    caption = RichTextField()
    caption_fr = RichTextField(blank=True, null=True)
    image = models.FileField(
        upload_to=image_directory_path)

    @property
    def get_caption(self):
        language = get_language()
        if language == 'fr' and self.caption_fr:
            return self.caption_fr
        return self.caption

    def __str__(self) -> str:
        return self.get_caption
