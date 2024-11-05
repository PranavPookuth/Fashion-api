from pickle import FALSE
from tkinter import Image

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Permission, Group, PermissionsMixin
from django.db import models



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True,default="123456789")
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_secret_key = models.CharField(max_length=32, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    road_name = models.TextField(default="road name")
    pincode = models.IntegerField(null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number', 'name']

    objects = CustomUserManager()

    # Define groups with a unique related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to avoid clashes
        blank=True
    )

    # Define user_permissions with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change this to avoid clashes
        blank=True
    )

    def __str__(self):
        return self.email


class PasswordResetUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    otp_secret_key = models.CharField(max_length=32, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='passwordresetuser_set', blank=True, verbose_name=('groups'))
    user_permissions = models.ManyToManyField(Permission, related_name='passwordresetuser_set', blank=True,
                                              verbose_name=('user permissions'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class products(models.Model):
    product_name = models.CharField(max_length=100,null=False)
    Description = models.CharField(max_length=100, null=False)
    product_image=models.ImageField(upload_to=Image,null=False)