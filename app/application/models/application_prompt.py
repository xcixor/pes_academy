from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from application.models import Application
from agripitch.models import SubCriteriaItem

User = get_user_model()


class ApplicationPrompt(models.Model):

    message = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='prompts')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE)
    prompt = models.ForeignKey(
        SubCriteriaItem, on_delete=models.CASCADE, related_name='prompts')

    def __str__(self) -> str:
        return _('Message for') + self.application.special_id +\
            _(' by') + str(self.reviewer)
