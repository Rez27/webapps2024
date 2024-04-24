from django.db import models
from register.models import User, UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone



# class UserProfile(models.Model):
#     CURRENCY_CHOICES = [
#         ('GBP', 'GBP'),
#         ('USD', 'USD'),
#         ('EUR', 'EUR'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payapp_profile')
#     bal = models.IntegerField(default=0)
#     currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
#
#     def __str__(self):
#         return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.register_profile.save()


class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.CASCADE)
    sent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=False)
    sent_currency = models.CharField(max_length=3, default='')
    received_currency = models.CharField(max_length=3, default='')

    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}: {self.sent_amount}"


class Notification(models.Model):
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    requested_currency = models.CharField(max_length=3, default='')
    timestamp = models.DateTimeField(auto_now_add=False, default=timezone.now)
    accepted_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
    rejected_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester.username} -> {self.receiver.username}: {self.amount} ({'Accepted' if self.is_accepted else 'Pending'})"
