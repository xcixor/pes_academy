from django.contrib.auth import get_user_model
from django.db import models
from application.models import Application

User = get_user_model()


class ApplicationPrompt(models.Model):

    message = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='prompts')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='prompts')

    def __str__(self) -> str:
        return f'Message for {self.application.special_id} by {self.reviewer}'
