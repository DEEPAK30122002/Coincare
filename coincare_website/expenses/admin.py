"""
Django admin configuration for the Expenses app.
"""

from django.contrib import admin
from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Expense model.
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
    list_per_page = 15


# Register models with the admin site
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
