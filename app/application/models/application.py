from django.db import models
from django.contrib.auth import get_user_model

from application.models.call_to_action import CallToAction


User = get_user_model()


class Application(models.Model):

    application_creator = models.OneToOneField(
        User, related_name='application', on_delete=models.CASCADE)
    call_to_action = models.ForeignKey(
        CallToAction, related_name='applications',
        on_delete=models.SET_NULL,
        null=True)
