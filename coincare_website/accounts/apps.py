"""
This contains the configuration for the Accounts application.
"""
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Configuration class for the Accounts.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals
