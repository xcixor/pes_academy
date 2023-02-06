from django.db import models
from academy.models import Session
from accounts.models import User


class SessionChatHistory(models.Model):

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='session_history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='session_history'
    )
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    class Meta:

        ordering = ('timestamp',)
        verbose_name_plural = 'Sessions Chat History'
