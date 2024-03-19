from django.db import models
from register.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payapp_profile')
    bal = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.payapp_profile.save()


class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}: {self.amount}"
