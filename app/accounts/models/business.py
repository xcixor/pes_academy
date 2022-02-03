from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BusinessOrganization(models.Model):

    VALUE_CHAIN_CHOICES = [
        ('chain_one', 'Primary production (farming)'),
        ('chain_two', 'Input supplier'),
        ('chain_three', 'Processor (value addition)'),
        ('chain_four', 'Aggregator'), ('chain_five', 'Distributor'),
        ('chain_six', 'Retailer'), ('chain_seven', 'Service provider')]

    EXISTENCE_PERIOD_CHOICES = [
        ('period_one', 'Below 1 year'),
        ('period_two', 'More than 1 year but less than 2 years'),
        ('period_three', 'Between 2 to 5 years'),
        ('period_four', 'Over 5 years')]

    STAGE_CHOICES = [
        ('stage_one', 'Product or service is still being developed'),
        ('stage_two', 'Product or service is at MVP stage. Currently piloting with target users'),
        ('stage_three', 'Product or service has been availed in the market. There are no sales or revenues as yet'),
        ('stage_four', 'Product or service is in the market. There are sales/revenues')]

    organization_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='businesses')
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
