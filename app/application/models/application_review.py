from django.db import models
from django.contrib.auth import get_user_model
from application.models import Application

User = get_user_model()


class ApplicationReview(models.Model):

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
