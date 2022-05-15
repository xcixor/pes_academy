from django.db import models
from staff.models import Session


def image_directory_path(instance, filename):
    return (f'sessions/{instance.session}/{filename}')


class SessionMaterial(models.Model):

    material_name = models.CharField(max_length=200)
    material = models.FileField(
        upload_to=image_directory_path)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE,
        related_name='materials')
    created = models.DateTimeField(
        auto_now_add=True)

    def __str__(self) -> str:
        return self.material_name
