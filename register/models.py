from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    currency = models.CharField(max_length=20, choices=[('GBP', 'GBP'), ('Euro', 'Euro'), ('Dollar', 'Dollar')], default='GBP')


def __str__(self):
    return self.user.username
