from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone = models.PositiveIntegerField(unique=True, null=True, blank=True)
    verify_code = models.PositiveSmallIntegerField(null=True, blank=True)
    expire_code = models.DateTimeField(null=True, blank=True)


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'
