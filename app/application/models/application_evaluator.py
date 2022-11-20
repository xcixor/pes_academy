from django.db import models
from django.contrib.auth import get_user_model
from application.models import Application

User = get_user_model()


class ApplicationEvaluator(models.Model):

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='evaluators')
    evaluator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='evaluations')

    def __str__(self):
        return f'{self.evaluator.username} - {self.application.special_id}'
