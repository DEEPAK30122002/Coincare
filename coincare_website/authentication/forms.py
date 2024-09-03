"""
Forms for user management in the CoinCare application.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """
    A form for creating a new user with additional fields for first name,
    last name, and email.
    """

    usable_password = None
    email = forms.EmailField(max_length=50, help_text="Enter your email address")

    class Meta:
        """
        Metadata for the SignupForm class.
        Specifies the model to be used and the fields to be included in the form.
        """

        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        """
        Save the user with additional fields (email, first name, last name).
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
