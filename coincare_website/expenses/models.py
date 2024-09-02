"""
Models for the Expenses app.

This module defines the data models for the Expenses application, including
the Expense and Category models. These models represent the data structure
used in the application and define the fields and relationships between them.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Expense(models.Model):
    """
    Represents an expense record.

    This model stores details about an expense, including the amount, date,
    description, owner, and category. It is linked to a User and includes
    a string representation method that returns the expense's description.
    """

    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)

    def __str__(self):
        """
        Return a string representation of the expense.

        This method returns the description of the expense.
        """
        return self.category

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    """
    Represents a category for expenses.

    This model stores the name of a category, used to classify expenses.
    It includes a string representation method that returns the category's name.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Return a string representation of the category.

        This method returns the name of the category.
        """
        return self.name
