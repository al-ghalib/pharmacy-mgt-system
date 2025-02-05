from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"

class IsSalesAssociate(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "sales"

class IsStockUpdater(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "stock_updater"

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "customer"

class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.status == "active"



# from rest_framework import permissions

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "admin"

# class IsSales(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ["admin", "sales"]

# class IsStockUpdater(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ["admin", "stock_updater"]


