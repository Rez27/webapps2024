from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

#Post Migrate signal function to create admin user on initial migration
@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    if kwargs.get('app_config').name == 'register':  # Ensure the signal is triggered only for the register app
        from django.contrib.auth.models import User  # Conditional Import to avoid circular import issue
        if not User.objects.filter(username='admin').exists():  # Check if admin user doesn't exist
            admin_user = User.objects.create_superuser('admin', 'admin@gmc.com', 'admin', first_name='Admin', last_name='User')

            UserProfile = apps.get_model('register', 'UserProfile')  # Get the UserProfile model dynamically
            if not UserProfile.objects.filter(user=admin_user).exists():  # Check if UserProfile exist for admin user
                UserProfile.objects.create(user=admin_user, email='admin@gmc.com', currency='GBP', is_superuser=1, bal=1000)
            else: #IF exists update the UserProfile model with following data
                admin_profile = UserProfile.objects.get(user=admin_user)
                admin_profile.email = 'admin@gmc.com'
                admin_profile.currency = 'GBP'
                admin_profile.is_superuser = True
                admin_profile.bal = 1000
                admin_profile.save()