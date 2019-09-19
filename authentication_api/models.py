from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for User model"""
    def create_user(self, email, username, password=None):
        """Function for creating a user"""
        if not email:
            return ValueError("Email must be provided")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Function for creating superusers"""
        user = self.create_user(email, username, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User database model"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    upvotes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    





