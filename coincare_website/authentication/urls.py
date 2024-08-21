"""
URL configurations for the authentication app in the CoinCare application.

This module defines the URL patterns for the authentication app, including
routes for user registration and login.
"""

from django.urls import path
from .views import RegistrationView, LoginView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
