"""
URL patterns for the UserPreferences app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="preferences"),
]
