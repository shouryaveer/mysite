from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image
from src.utils import hex_uuid

# Create your models here.

class UserManager(BaseUserManager):


    def create_user(self, username, email, password, first_name, last_name):
        """
        Create User with username, email & password
        """
        if not username:
            raise ValueError('Users Must have a username')
        if not email:
            raise ValueError('Users must have an email')
        
        if password is None:
            raise TypeError('Users must have a password')
        
        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.id = hex_uuid()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, first_name=None, last_name=None):
        """
        Create a superuser with admin privileges
        """
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(username, email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=hex_uuid, editable=False, unique=True)
    username = models.CharField(verbose_name='username', max_length=20, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50, unique=False, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, unique=False, null=True, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=hex_uuid, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(verbose_name="First Name", max_length=50, unique=False, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile-pics/', null=True, blank=True)
    followers_count = models.PositiveBigIntegerField(verbose_name="Followers Count", default=0)
    following_count = models.PositiveBigIntegerField(verbose_name="Following Count", default=0)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return "{} Profile".format(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_pic and self.profile_pic is not None:
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)

class UserFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")

    class Meta:
        db_table = "user_followers"