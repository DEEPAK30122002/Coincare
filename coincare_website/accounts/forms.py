from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
