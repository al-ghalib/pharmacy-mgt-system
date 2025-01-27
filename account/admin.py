from django.contrib import admin
from .models import User, Organization, OrganizationUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'phone', 'status', 'organization', 'is_staff', 'is_superuser']
    list_filter = ['status', 'organization']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'gender', 'image', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Organization', {'fields': ('organization',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'gender', 'image', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'address', 'trade_licence', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']
    ordering = ['name']

admin.site.register(Organization, OrganizationAdmin)


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'status', 'salary']
    search_fields = ['user__email', 'organization__name']
    list_filter = ['status', 'organization']
    ordering = ['organization', 'user']

admin.site.register(OrganizationUser, OrganizationUserAdmin)
