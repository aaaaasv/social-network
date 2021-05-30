from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_request = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_joined']
