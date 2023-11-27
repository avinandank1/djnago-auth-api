
from django.apps import AppConfig
from django.db import models  # Add this line

class AuthApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_api'

    def ready(self):
        # Import the signal handler here to avoid circular import
        from .signals import User_Profile_group_Creation
        # Connect the signal
        models.signals.post_save.connect(User_Profile_group_Creation, sender=self.get_model('User'))
