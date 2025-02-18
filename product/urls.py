from django.urls import path
from .views import (
    CategoryListCreateView,
    MedicineListCreateView,
    InventoryListCreateView,
    InventoryRetrieveUpdateDestroyView,
    InventoryStockUpdateView,
)

urlpatterns = [
    path("categories", CategoryListCreateView.as_view(), name="category-list-create"),
    path("medicines", MedicineListCreateView.as_view(), name="medicine-list-create"),
    path(
        "inventory",
        InventoryListCreateView.as_view(),
        name="inventory-list-create",
    ),
    path(
        "inventory/<uuid:uid>",
        InventoryRetrieveUpdateDestroyView.as_view(),
        name="inventory-retrieve-update-destroy",
    ),
    path(
        "inventory/<uuid:uid>/update-stock",
        InventoryStockUpdateView.as_view(),
        name="inventory-stock-update",
    ),
]