from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    currency = models.CharField(max_length=20, choices=[('GBP', 'GBP'), ('Euro', 'EUR'), ('Dollar', 'USD')], default='GBP')
    is_superuser = models.BooleanField(default=False)
    bank_account = models.CharField(max_length=8, unique=True)  # New field for the bank account number




def __str__(self):
    return self.user.username
