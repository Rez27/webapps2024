from django.contrib.auth.models import User
from django.db.models import Q


def user_email_check(email):
    return len(User.objects.filter(email=email)) > 0


def username_check(username):
    return len(User.objects.filter(username=username)) > 0

