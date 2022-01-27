from django.db import models
from accounts.models import BusinessOrganization


class CovidImpact(models.Model):
    business = models.OneToOneField(
        BusinessOrganization, on_delete=models.CASCADE,
        related_name='covid_impact')
    impact_one = models.TextField()
    impact_two = models.TextField(null=True)
