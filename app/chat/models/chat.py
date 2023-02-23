from django.db import models
from academy.models import Session
from accounts.models import User, Coach


class SessionChatHistory(models.Model):

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='chat_history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_history'
    )
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    class Meta:

        ordering = ('timestamp',)
        verbose_name_plural = 'Sessions Chat History'


class CoachChatHistory(models.Model):

    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        related_name='chat_history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='coaching_chat_history'
    )
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    class Meta:

        ordering = ('timestamp',)
        verbose_name_plural = 'Sessions Chat History'
