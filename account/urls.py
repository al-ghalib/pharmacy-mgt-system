# from django.urls import path
# from .views import UpdateStockView, CustomerTransactionView, AdminDashboardView

# urlpatterns = [
#     path('update-stock/', UpdateStockView.as_view(), name='update-stock'),
#     path('customer-transaction/', CustomerTransactionView.as_view(), name='customer-transaction'),
#     path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

#     #  path('medicines/', ViewMedicine.as_view({'get': 'list'}), name='view_medicines'),
#     # path('medicines/<uuid:pk>/', ViewMedicine.as_view({'get': 'retrieve'}), name='view_a_medicine'),
#     # path('inventory/', ViewInventory.as_view({'get': 'list'}), name='view_inventory'),
#     # path('inventory/<uuid:pk>/', ViewInventory.as_view({'get': 'retrieve'}), name='view_an_inventory'),
#     # path('inventory/check_stock/', ViewInventory.as_view({'get': 'check_stock'}), name='view_branch_in_stock'),
# ]

from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    OrganizationListCreateView,
    OrganizationDetailView,
    OrganizationUserListCreateView,
    OrganizationUserDetailView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization-users/', OrganizationUserListCreateView.as_view(), name='organization-user-list-create'),
    path('organization-users/<int:pk>/', OrganizationUserDetailView.as_view(), name='organization-user-detail'),
]
