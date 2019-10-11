from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models import UniqueConstraint


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
    

class Community(models.Model):
    """DB Model for Community"""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_members = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class UserJoinedCommunity(models.Model):
    """DB Model for users joined communities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'community'], name="user-joined-community")
        ]

    def __str__(self):
        return f"{self.user.username}|{self.community.name}"


class Post(models.Model):
    """DB Model for Post"""
    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """DB model for Comments"""
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'post'], name="user-upvoted-post")
        ]

    
    def __str__(self):
        return f"{self.user.username}|{self.post.title}"

