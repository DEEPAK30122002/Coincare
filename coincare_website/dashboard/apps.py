"""
This module contains the configuration for the Dashboard application.
"""

from django.apps import AppConfig

class DashboardConfig(AppConfig):
    """
    Configuration for the Dashboard application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
