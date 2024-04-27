from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from register.models import UserProfile


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    # Check if this is the initial migration
    if kwargs.get('app') == 'register' and kwargs.get('created_models'):
        # Check if User model is created
        if User in kwargs['created_models']:
            # Create default admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                first_name='admin',
                last_name='admin',
                email='admin@gmc.com',
                is_superuser=True,
                is_staff=True
            )
            if created:
                admin_user.set_password('admin')  # Set default password
                admin_user.save()

            # Create default admin UserProfile
            admin_profile, created = UserProfile.objects.get_or_create(
                user=admin_user,
                email='admin@gmc.com',
                currency='GBP',
                is_superuser=True,
                bal=1000
            )
