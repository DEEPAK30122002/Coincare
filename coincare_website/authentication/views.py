"""
Views for the authentication app in the CoinCare application.

This module contains views for user registration and login, including the
logic for handling GET and POST requests for each view.
"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from authentication.forms import SignupForm


class RegistrationView(View):
    """
    View for user registration.

    Handles the display and processing of the registration form.
    """

    def get(self, request):
        """
        Handle GET requests to display the registration form.

        Returns:
        HttpResponse: The rendered registration form.
        """
        form = SignupForm()
        return render(request, "authentication/register.html", {"form": form})

    def post(self, request):
        """
        Handle POST requests to process the registration form.

        Returns:
        HttpResponse: Redirect to the login page on success or re-render
                      the registration form with errors.
        """
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "login"
            )  # Redirect to the login page after successful registration
        return render(request, "authentication/register.html", {"form": form})


class LoginView(View):
    """
    View for user login.

    Handles the display and processing of the login form.
    """

    def get(self, request):
        """
        Handle GET requests to display the login form.

        Returns:
        HttpResponse: The rendered login form.
        """
        form = AuthenticationForm()
        return render(request, "authentication/login.html", {"form": form})

    def post(self, request):
        """
        Handle POST requests to process the login form.

        Returns:
        HttpResponse: Redirect to a success page on successful login or
                      re-render the login form with errors.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("base")  # Redirect to a success page after login
            form.add_error(None, "Invalid username or password.")
        return render(request, "authentication/login.html", {"form": form})
