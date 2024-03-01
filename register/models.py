from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency_choices = [
        ('GBP', 'British Pounds'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Consider using DecimalField for currency

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
