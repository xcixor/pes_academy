from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from application.models import Application


User = get_user_model()


class ApplicationComment(models.Model):

    comment = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='comments')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return _('Comment for ') + self.application.special_id + \
            _(' by') + self.reviewer
