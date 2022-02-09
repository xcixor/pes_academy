from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email, and password.
        """
        if not username:
            raise ValueError('A User must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    LANGUAGE_CHOICES = [
        ('english', 'English'), ('french', 'French'),
        ('portuguese', 'Portuguese')]
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'),
                      ('undisclosed', 'Prefer not to say'), ('other', 'Other')]
    AGE_CHOICES = [
        ('range_one', '20-29'), ('range_two', '30-39'),
        ('range_three', '40-49'), ('range_four', 'Above 50')]

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(
        verbose_name='Primary Email Address', max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    age = models.CharField(null=True, choices=AGE_CHOICES, max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    preferred_language = models.CharField(
        max_length=40, choices=LANGUAGE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.full_name
