from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Coach(models.Model):

    coach = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentees')
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='coaches')

    class Meta:

        verbose_name_plural = 'Coaches'

    def __str__(self) -> str:
        return f'Coach: {self.coach} - Mentee: {self.mentee}'
