from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Coach(models.Model):

    TYPES_OF_COACHES = (
        ('psa', _('PSA')),
        ('support', _('SUPPORT'))
    )

    coach = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentees')
    type = models.CharField(
        verbose_name=_('Type of Coach'),
        choices=TYPES_OF_COACHES,
        default='psa',
        max_length=100
    )
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='coaches')

    class Meta:

        verbose_name_plural = 'Coaches'
        unique_together = [['coach', 'mentee']]

    def __str__(self) -> str:
        return f'Coach: {self.coach} - Mentee: {self.mentee}'
