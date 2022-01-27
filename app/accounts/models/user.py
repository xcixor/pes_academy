from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, email_address, password, **extra_fields):
        """
        Creates and saves a User with the given email_address, and password.
        """
        if not email_address:
            raise ValueError('Please provide an email address')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email_address, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    LANGUAGE_CHOICES = [
        ('english', 'English'), ('french', 'French'),
        ('portuguese', 'Portuguese')]
    GENDER_CHOICES = [('male', 'Male'), ('femail', 'Female'),
                      ('undisclosed', 'Prefer not to say'), ('other', 'Other')]

    email_address = models.EmailField(
        verbose_name='Primary Email Address', max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    native_language = models.CharField(max_length=40, choices=LANGUAGE_CHOICES)
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    preferred_language = models.CharField(
        max_length=40, choices=LANGUAGE_CHOICES)
    preferred_email_address = models.EmailField(
        verbose_name='Preferred Email Address', max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'

    def __str__(self) -> str:
        return self.full_name
