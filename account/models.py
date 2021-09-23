from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
