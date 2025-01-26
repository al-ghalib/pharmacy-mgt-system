from django.contrib import admin
from .models import User, Organization, OrganizationUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "organization", "is_staff"]
    search_fields = ["email", "organization__name"]
    list_filter = ["role", "is_staff"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "is_admin"]
    search_fields = ["user__email", "organization__name"]
    list_filter = ["is_admin"]
