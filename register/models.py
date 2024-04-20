from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='register_profile')
    email = models.EmailField()
    currency = models.CharField(max_length=20, choices=[('GBP', 'GBP'), ('Euro', 'EUR'), ('Dollar', 'USD')])
    is_superuser = models.BooleanField(default=False)

    bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)


def __str__(self):
    return self.user.username

