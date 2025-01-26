from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"


class IsStockUpdater(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "stock_updater"


class IsSalesAssociate(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "sales"
