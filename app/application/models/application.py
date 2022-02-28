from django.db import models
from django.contrib.auth import get_user_model

from application.models.call_to_action import CallToAction


User = get_user_model()


class Application(models.Model):

    STATUS_CHOICES = (
        ('step_one', 'Application Data Not Submitted'),
        ('step_two', 'Documents in review'),
        ('step_three', 'Approved')
    )

    application_creator = models.OneToOneField(
        User, related_name='application', on_delete=models.CASCADE)
    call_to_action = models.ForeignKey(
        CallToAction, related_name='applications',
        on_delete=models.SET_NULL,
        null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='step_one',
        max_length=100
    )
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text='Unique text to append to the address for the application.')

    def __str__(self) -> str:
        return f'{self.call_to_action} - {self.application_creator}'
