"""
This module contains views for user authentication.
"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from authentication.forms import SignupForm
class RegistrationView(View):
    """
    Handles displaying and processing the registration form.
    """
    def get(self, request):
        """
        Displays the registration form.
        """
        form = SignupForm()
        return render(request, "authentication/register.html", {"form": form})

    def post(self, request):
        """
        Processes the registration form submission.
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
    Handles displaying and processing the login form.
    """
    def get(self, request):
        """
        Displays the login form.
        """
        form = AuthenticationForm()
        return render(request, "authentication/login.html", {"form": form})

    def post(self, request):
        """
        Processes the login form submission.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")  # Redirect to a success page after login
            else:
                form.add_error(None, "Invalid username or password.")
        return render(request, "authentication/login.html", {"form": form})
