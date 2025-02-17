from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Organization, OrganizationUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone",
        "status",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["status", "is_staff", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    readonly_fields = ["last_login", "date_joined"]
    filter_horizontal = ["groups", "user_permissions"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "address",
                    "gender",
                    "image",
                )
            },
        ),
        (
            "Status",
            {
                "fields": ("status",),
                "description": "Manage the user's status in the system.",
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_superuser"),
                "description": "Control the user's permissions and access levels.",
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
                "description": "Track important dates related to the user.",
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone",
                    "address",
                    "gender",
                    "image",
                    "status",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "email",
        "address",
        "trade_licence",
        "has_active_members",
    ]
    list_filter = []
    search_fields = ["name", "email"]
    ordering = ["name"]

    @admin.display(description="Active Members", boolean=True)
    def has_active_members(self, obj):
        return obj.organization_users.filter(status="active").exists()


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "organization",
        "role",
        "status",
        "salary",
    ]
    list_filter = ["status", "role"]
    search_fields = ["user__email", "organization__name"]
    ordering = ["organization", "user"]
