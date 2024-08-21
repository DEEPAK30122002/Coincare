"""
URL patterns for the Expenses app.

This module defines the URL routes for handling expense-related views, 
including listing, adding, editing, deleting, and searching expenses. 
It also includes routes for expense summaries and statistics.
"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add-expense", views.add_expense, name="add-expenses"),
    path("edit-expense/<int:id>", views.expense_edit, name="expense-edit"),
    path("expense-delete/<int:id>", views.delete_expense, name="expense-delete"),
    path(
        "search-expenses/", csrf_exempt(views.search_expenses), name="search_expenses"
    ),
    path(
        "expense_category_summary",
        views.expense_category_summary,
        name="expense_category_summary",
    ),
    path("stats", views.stats_view, name="stats"),
]
