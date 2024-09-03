"""
This module contains the models for the Accounts application.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Model to store additional profile information for users, such as profile pictures.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
