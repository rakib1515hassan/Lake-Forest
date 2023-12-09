from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import UserOTP, Occupation, Academic
from django.contrib.auth import get_user_model

User = get_user_model()

from apps.users.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["id", "name", "email", "is_verified", "role"]
    list_filter = ["is_verified", "role"]
    fieldsets = [
        (None, {"fields": ["email", "password", "created_at", "updated_at"]}),
        (
            "Personal info",
            {"fields": ["name", "phone", "profile_img", "dob", "gender"]},
        ),
        # ("Personal Address", {"fields": ['division', 'sub_division', 'zip_code', 'home']}),
        (
            "Permissions",
            {
                "fields": [
                    "is_superuser",
                    "is_admin",
                    "is_active",
                    "is_verified",
                    "role",
                ]
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password",
                    "password2",
                    "is_verified",
                    "name",
                    "phone",
                    "profile_img",
                    "role",
                    "dob",
                    "gender",
                ],
            },
        ),
    ]
    search_fields = ["email", "name"]

    ordering = ["-created_at", "email"]  # Latest users first, then by email

    filter_horizontal = []  ## 'filter_horizontal[0]' must be a many-to-many field.

    readonly_fields = ["created_at", "updated_at"]  # Add these readonly fields


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Occupation)
admin.site.register(Academic)


@admin.register(UserOTP)
class UserOTP_Admin(admin.ModelAdmin):
    list_display = ("id", "Email", "otp", "is_used", "created_at")

    def Email(self, obj):
        return obj.user.email

    Email.short_description = "Email"


# @admin.register(UserAddress)
# class UserOTP_Admin(admin.ModelAdmin):
#     list_display = ( 'id','Email', 'division')

#     def Email(self, obj):
#         return obj.user.email

#     Email.short_description = 'Email'
