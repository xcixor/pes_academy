from django.db import models
from application.models import BusinessOrganization


class Milestone(models.Model):
    milestone = models.CharField(max_length=255)
    businesses = models.ManyToManyField(
        BusinessOrganization, blank=True, related_name='businesses')

    def __str__(self) -> str:
        return self.milestone