from rest_framework import permissions
from .models import RoleChoices


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.organization_memberships.filter(
                role=RoleChoices.ADMIN
            ).exists()
        )


class IsSalesAssociate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.organization_memberships.filter(
                role=RoleChoices.SALES
            ).exists()
        )


class IsStockUpdater(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.organization_memberships.filter(
                role=RoleChoices.STOCK_UPDATER
            ).exists()
        )


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.organization_memberships.filter(
                role=RoleChoices.CUSTOMER
            ).exists()
        )


class IsOrganizationStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.organization_memberships.filter(
                role__in=[
                    RoleChoices.ADMIN,
                    RoleChoices.SALES,
                    RoleChoices.STOCK_UPDATER,
                ]
            ).exists()
        )


class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.status == "ACTIVE"
        )


