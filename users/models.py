from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.base_user import  BaseUserManager

# Create your models here.

## Custom User Manager
class CustomUserManager(BaseUserManager):
    """The custome user manager is used to
    make emails the unique identifiers for authentication,
    instead of username
    """
    
    def create_user(self, email, password, **extra_fields):
        """function to create a save a user"""
        if not email:
            raise ValueError("The Email must be given")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """function to create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


## Custom User
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, default=0)
    image = models.ImageField(upload_to='profile_pictures/', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
