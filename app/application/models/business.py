from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class BusinessOrganization(models.Model):

    VALUE_CHAIN_CHOICES = [
        ('chain_one', _('Primary production (farming)')),
        ('chain_two', _('Input supplier')),
        ('chain_three', _('Processor (value addition)')),
        ('chain_four', _('Aggregator')),
        ('chain_five', _('Distributor')),
        ('chain_six', _('Retailer')),
        ('chain_seven', _('Service provider'))]

    EXISTENCE_PERIOD_CHOICES = [
        ('period_one', _('Below 1 year')),
        ('period_two', _('More than 1 year but less than 2 years')),
        ('period_three', _('Between 2 to 5 years')),
        ('period_four', _('Over 5 years'))]

    STAGE_CHOICES = [
        ('stage_one', _('Product or service is still being developed')),
        ('stage_two', _(
            'Product or service is at MVP stage. Currently piloting with target users')),
        ('stage_three', _(
            'Product or service has been availed in the market. There are no sales or revenues as yet')),
        ('stage_four', _('Product or service is in the market. There are sales/revenues'))]

    organization_owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='business')
    organization_name = models.CharField(max_length=255)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    whatsapp_business_link = models.URLField(null=True, blank=True)
    value_chain = models.CharField(max_length=255, choices=VALUE_CHAIN_CHOICES)
    existence_period = models.CharField(
        max_length=255, choices=EXISTENCE_PERIOD_CHOICES)
    stage = models.CharField(max_length=255, choices=STAGE_CHOICES)

    def __str__(self) -> str:
        return self.organization_name
