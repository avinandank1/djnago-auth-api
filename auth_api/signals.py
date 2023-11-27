# Import necessary modules and classes
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

# Define a signal receiver function for post-save
@receiver(post_save, sender=User)
def User_Profile_group_Creation(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile and assign them to a custom group based on their role.

    Args:
        sender: The model class that sent the signal (User in this case).
        instance: The actual instance of the model that was saved.
        created: A boolean indicating whether the instance was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    # Check if a new user instance was created
    if created:
        # Choose unique names for the groups to avoid conflicts
        admin_group_name = 'AdminProfile'
        user_group_name = 'UserProfile'
        
        # Check if the user is an admin
        if instance.is_admin:
            # Get or create the admin group and add the user to it
            admin_group, created = Group.objects.get_or_create(name=admin_group_name)
            instance.groups.add(admin_group)
        else:
            # Get or create the user profile group and add the user to it
            user_group, created = Group.objects.get_or_create(name=user_group_name)
            instance.groups.add(user_group)
        
        # Create a profile for the user
        Profile.objects.create(user=instance)
