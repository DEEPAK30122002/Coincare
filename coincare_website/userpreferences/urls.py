"""
URL patterns for the UserPreferences app.

This module defines the URL routing for the UserPreferences app,
including the view for displaying user preferences.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="preferences"),
]
