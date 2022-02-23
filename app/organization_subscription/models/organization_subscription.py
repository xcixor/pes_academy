from django.db import models
from django.contrib.auth import get_user_model
from application.models import BusinessOrganization


User = get_user_model()


class OrganizationSubscription(models.Model):

    subscription_creator = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organization_admin')

    organization = models.OneToOneField(
        BusinessOrganization,
        on_delete=models.SET_NULL,
        related_name='organization',
        null=True,
        blank=True)

    @property
    def organization_subscription_id(self):
        return f'BUS-{self.id}'

    def __str__(self) -> str:
        return self.organization_subscription_id
