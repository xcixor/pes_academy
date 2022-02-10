from django.db import models
from application.models import BusinessOrganization


class CovidImpact(models.Model):
    business = models.OneToOneField(
        BusinessOrganization, on_delete=models.CASCADE,
        related_name='covid_impact')
    impact = models.TextField()
