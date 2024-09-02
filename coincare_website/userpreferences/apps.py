"""
Configuration for the UserPreferences app.

This module defines the configuration class for the UserPreferences app,
which handles user-specific preferences within the application.
"""

from django.apps import AppConfig


class UserpreferencesConfig(AppConfig):
    """
    Configuration for the UserPreferences app.

    This class is used to configure the UserPreferences app, including
    specifying the default auto field type and the app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "userpreferences"
