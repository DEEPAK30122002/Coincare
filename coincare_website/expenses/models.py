"""
Models for the Expenses app.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Expense(models.Model):
    """
    Represents an expense record.
    """

    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)

    def __str__(self):
        """
        Return a string representation of the expense.
        """
        return self.category

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    """
    Represents a category for expenses.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Return a string representation of the category.
        """
        return self.name
