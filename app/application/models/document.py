from django.db import models
from application.models import Application


def image_directory_path(instance, filename):
    return (f'applications/{instance.application}/{filename}')


class ApplicationDocument(models.Model):

    document_name = models.CharField(max_length=200)
    document = models.FileField(
        upload_to=image_directory_path)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='documents')

    def __str__(self) -> str:
        return self.document_name
