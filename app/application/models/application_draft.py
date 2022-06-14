from django.db import models
from application.models import Application


class ApplicationDraftData(models.Model):

    application = models.OneToOneField(
        Application, on_delete=models.DO_NOTHING,
        null=True, blank=True, related_name='draft')
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    whatsapp_business_link = models.URLField(null=True, blank=True)
    value_chain = models.CharField(max_length=100, blank=True, null=True)
    existence_period = models.CharField(max_length=100, blank=True, null=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    milestones = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'Draft for {self.application}'
