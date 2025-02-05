from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, OrganizationUser

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'phone', 'status', 'role', 
        'is_staff', 'is_superuser', 'is_active_status'
    ]
    list_filter = ['status', 'role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ['groups', 'user_permissions']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'address', 'gender', 'image')
        }),
        ('Status & Role', {
            'fields': ('status', 'role'),
            'description': "Manage the user's status and role in the system."
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': "Control the user's permissions and access levels."
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
            'description': "Track important dates related to the user."
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name', 
                'phone', 'address', 'gender', 'image', 'status', 'role', 
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

    @admin.display(description="Is Active?", boolean=True)
    def is_active_status(self, obj):
        """Display whether the user is active."""
        return obj.status == "active"


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'address', 'trade_licence', 'has_active_members']
    list_filter = []
    search_fields = ['name', 'email']
    ordering = ['name']

    @admin.display(description="Active Members", boolean=True)
    def has_active_members(self, obj):
        """Check if the organization has active members."""
        return obj.organization_users.filter(status="active").exists()


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'status', 'salary', 'is_active_member']
    list_filter = ['status', 'role']
    search_fields = ['user__email', 'organization__name']
    ordering = ['organization', 'user']

    @admin.display(description="Is Active Member?", boolean=True)
    def is_active_member(self, obj):
        """Display whether the user is an active member of the organization."""
        return obj.status == "active"