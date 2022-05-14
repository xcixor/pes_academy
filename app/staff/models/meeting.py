from django.db import models
from staff.models import Session


class Meeting(models.Model):

    session = models.ForeignKey(
        Session, on_delete=models.CASCADE,
        related_name='meetings')
    link = models.URLField(unique=True)

    @property
    def special_id(self):
        filled_id = f'{self.id}'.zfill(3)
        return f'MEET - {filled_id}'

    def __str__(self) -> str:
        return self.special_id
