"""
Django admin configuration for the Expenses app.

This module registers the models from the Expenses app with the Django admin
site, allowing them to be managed through the admin interface.
"""

from django.contrib import admin
from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Expense model.

    This class customizes the admin interface for managing Expense instances,
    list view and how to search for
    records.
    """

    list_display = (
        "amount",
        "description",
        "owner",
        "category",
        "date",
    )
    search_fields = (
        "description",
        "category",
        "date",
    )
    list_per_page = 5


# Register models with the admin site
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
