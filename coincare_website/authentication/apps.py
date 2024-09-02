"""
This module contains the configuration for the authentication app.

It includes the AuthenticationConfig class, which is used to configure
the authentication application for the Django project.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration for the authentication app.

    This class sets up the application configuration for 
    the 'authentication' app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
