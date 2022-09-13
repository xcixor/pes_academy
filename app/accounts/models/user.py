from operator import mod
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email, and password.
        """
        if not username:
            raise ValueError(_('A User must have a username'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_temporal_user(self, email, **extra_fields):
        user = self.model(email=email, username=email, **extra_fields)
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
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(username, password, **extra_fields)

    def get_user_by_uid(self, uidb64):
        """
        Return a user object based on the user's id encoded in base 64.
        """
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = self.get_queryset().get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None
        return user


def image_directory_path(instance, filename):
    return (f'accounts/{instance.email}/{filename}')


class User(AbstractBaseUser, PermissionsMixin):

    LANGUAGE_CHOICES = [
        ('english', _('English')),
        ('french', _('French')),
        ('portuguese', _('Portuguese'))]
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('undisclosed', _('Prefer not to say')),
        ('other', _('Other'))]
    AGE_CHOICES = [
        ('range_one', _('20-29')),
        ('range_two', _('30-39')),
        ('range_three', _('40-49')),
        ('range_four', _('Above 50'))]

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(
        verbose_name=_('Email Address'), max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_applying_for_a_call_to_action = models.BooleanField(default=False)
    age = models.CharField(null=True, choices=AGE_CHOICES, max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    preferred_language = models.CharField(
        max_length=40, choices=LANGUAGE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    linked_in = models.URLField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=image_directory_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        if self.is_applying_for_a_call_to_action:
            return 'AfDB-' + str(self.id).zfill(3)
        return str(self.id).zfill(3)
