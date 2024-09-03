"""
This module contains views for the Accounts application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile


@login_required
def profile(request):
    """
    View function to display and update the user's profile.
    """
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=user_profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=user_profile)

    context = {"u_form": u_form, "p_form": p_form, "user_profile": user_profile}

    return render(request, "accounts/profile.html", context)
