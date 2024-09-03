"""
This module contains forms for user and user profile management.
"""
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


class UserUpdateForm(forms.ModelForm):
    """
    A form for updating user information such as username, email, and name.
    """
    class Meta:
        """
        This contains username , email , first and last name of user.
        """
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserProfileUpdateForm(forms.ModelForm):
    """
    A form for updating profile picture.
    """
    class Meta:
        """
        This contains profile picture of user.
        """
        model = UserProfile
        fields = ["profile_picture"]
