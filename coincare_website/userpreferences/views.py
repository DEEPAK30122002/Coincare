"""
Views for the UserPreferences app.
"""
import os
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponseNotFound, HttpResponseBadRequest
from .models import UserPreference

def index(request):
    """
    Display and update user preferences for currency.
    """
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")

    # Check if the file exists
    if not os.path.isfile(file_path):
        return HttpResponseNotFound("Currency data file not found.")

    # Load currency data
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for name, value in data.items():
                currency_data.append({"name": name, "value": value})
    except json.JSONDecodeError:
        messages.error(request, "Error decoding currency data file.")
        return render(request, "preferences/index.html", {"currencies": currency_data})

    # Retrieve or create user preferences
    user_preferences, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == "POST":
        currency = request.POST.get("currency")
        if currency:
            user_preferences.currency = currency
            user_preferences.save()
            messages.success(request, "Changes saved successfully.")
            return redirect("preferences")  # Redirect to avoid form resubmission
        else:
            messages.error(request, "Please select a currency.")

    return render(
        request,
        "preferences/index.html",
        {"currencies": currency_data, "user_preferences": user_preferences},
    )
