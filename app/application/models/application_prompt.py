from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from application.models import Application

User = get_user_model()


class ApplicationPrompt(models.Model):

    message = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='prompts')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='prompts')
    question_position = models.IntegerField(
        help_text=_('The position of the question in the form'))

    def __str__(self) -> str:
        return _('Message for') + self.application.special_id +\
            _(' by') + str(self.reviewer)
