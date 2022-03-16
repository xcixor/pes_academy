from django.db import models
from django.contrib.auth import get_user_model
from application.models import Application


User = get_user_model()


class ScoreWeight(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'


class ApplicationScore(models.Model):

    score = models.IntegerField(
        default=ScoreWeight.LOW, choices=ScoreWeight.choices)
    prompt = models.TextField()
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='scores')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='scores')

    def __str__(self):
        return f'{self.get_score_display()} score for {self.prompt} for {self.application.special_id}'
