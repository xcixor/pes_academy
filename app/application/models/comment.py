from django.contrib.auth import get_user_model
from django.db import models
from application.models import Application


User = get_user_model()


class ApplicationComment(models.Model):

    comment = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='comments')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return f'Comment for {self.application.special_id} by {self.reviewer}'
