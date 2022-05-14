from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Session(models.Model):

    coach = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events')
    coachee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True)

    @property
    def special_id(self):
        filled_id = f'{self.id}'.zfill(3)
        return f'EVT - {filled_id}'

    def __str__(self) -> str:
        return self.title
