from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from application.models import Application


User = get_user_model()


class ScoreWeight(models.IntegerChoices):
    STRONGLY_DISAGREE = 1, _('Strongly Disagree')
    DISAGREE = 2, _('Disagree')
    NEUTRAL = 3, _('Neutral')
    AGREE = 4, _('Agree')
    STRONGLY_AGREE = 5, _('Strongly Agree')


class ApplicationScore(models.Model):

    score = models.IntegerField(
        default=ScoreWeight.STRONGLY_DISAGREE, choices=ScoreWeight.choices)
    prompt = models.TextField()
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='scores')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='scores')
    question_position = models.IntegerField(
        help_text=_('The position of the question in the form'))

    def __str__(self):
        return self.get_score_display() + \
            _('score for') + self.prompt + \
            _(' for') + self.application.special_id
