from django.db import models


def partner_logo_directory_path(instance, filename):
    return (f'carousel/{filename}')


class PartnerLogo(models.Model):

    title = models.CharField(max_length=400, unique=True)
    image = models.FileField(
        upload_to=partner_logo_directory_path)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    for_footer = models.BooleanField(default=False)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.title} Logo'

    class Meta:
        ordering = ['position']
        verbose_name_plural = '6 Partner Logos'
