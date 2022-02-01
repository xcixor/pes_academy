from django.db import models
from accounts.models import BusinessOrganization


class Milestone(models.Model):
    milestone = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.milestone


# businessesmilestonesmodel