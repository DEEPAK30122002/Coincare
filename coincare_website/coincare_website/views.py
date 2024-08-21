"""
Views for the CoinCare website.

This module contains view functions that handle HTTP requests and return
HTTP responses for various pages on the CoinCare website.
"""

from django.shortcuts import render


def index(request):
    """
    Render the index page.

    Returns:
    HttpResponse: The rendered index.html template.
    """
    return render(request, "index.html")
