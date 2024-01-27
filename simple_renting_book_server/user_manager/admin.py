from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from simple_renting_book_server.mixins import CollapsibleInlineMixin

from .forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import Profile, User


class ProfileInlineAdmin(CollapsibleInlineMixin, admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    inlines = (ProfileInlineAdmin,)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"classes": ("collapse",), "fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide", "collapse"),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
    )
    list_filter = (
        "is_superuser",
        "is_active",
    )
    readonly_fields = (
        "id",
        "date_joined",
        "is_staff",
    )
    search_fields = ("email",)
    ordering = ("email",)

    @admin.display(boolean=True)
    def is_staff(self, obj):
        return obj.is_staff
