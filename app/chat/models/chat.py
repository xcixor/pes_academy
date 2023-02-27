from django.db import models
from django.utils.translation import gettext_lazy as _
from academy.models import Session
from accounts.models import User, Coach


def session_image_directory_path(instance, filename):
    return (f'chat/session/{instance}/{filename}')


class SessionChatHistory(models.Model):

    MESSAGE_TYPES = (
        ('text', 'TEXT'),
        ('file', 'FILE')
    )

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
    file = models.ImageField(
        upload_to=session_image_directory_path, null=True, blank=True)
    timestamp = models.DateTimeField()
    type = models.CharField(
        verbose_name=_('Type of Message'),
        choices=MESSAGE_TYPES,
        default='text',
        max_length=100
    )

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
