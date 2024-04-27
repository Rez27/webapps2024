from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def superuser_required(function):
    """
    Decorator for views that checks whether the user is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='/webapps2024/login/'
    )
    return actual_decorator(function)
