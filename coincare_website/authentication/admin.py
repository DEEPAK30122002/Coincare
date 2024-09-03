"""
Admin configuration for the CoinCare application.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from authentication.forms import SignupForm  # Corrected import path


class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the User model.
    """

    # The forms to add and change user instances
    add_form = SignupForm
    form = SignupForm
    model = User
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


# Register the User model with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
