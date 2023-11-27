from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.urls import reverse
from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that extends AbstractBaseUser.
    """

    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        '''
        Returns the full name of the user.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def get_absolute_url(self):
        """
        Returns the URL to access a particular user instance.
        """
        return reverse('login', args=[str(self.id)])
    
    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @is_staff.setter
    def is_staff(self, value):
        """
        Set the user's staff status.
        """
        self.is_admin = value
    


class Profile(models.Model):
    """
    Profile model associated with the User model.
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=20)
    location = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the Profile instance.
        """
        return self.user.get_full_name()
