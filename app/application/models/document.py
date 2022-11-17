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

    def reviewer(self):
        if self.application.reviewers.all():
            return f'{self.application.reviewers.first().reviewer.email} : {self.application.reviewers.first().reviewer.username}'
        return "Not Assigned"

    def creator(self):
        return self.application.application_creator.email

    def __str__(self) -> str:
        return self.document_name

    class Meta:
        ordering = ['application__application_creator_id']
