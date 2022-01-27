from django.db import models
from accounts.models import BusinessOrganization


class Milestone(models.Model):
    business = models.ForeignKey(
        BusinessOrganization, on_delete=models.CASCADE,
        related_name='milestones')
    milestone = models.CharField(max_length=255)
