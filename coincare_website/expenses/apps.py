"""
Configuration for the Expenses app.

This module contains the configuration class for the Expenses application,
which is used to set up the app's configuration and metadata.
"""

from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    """
    Configuration for the Expenses application.

    This class configures the Expenses app,specifying the
    primary key field type and the name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "expenses"
