# from django.urls import path
# from .views import (
#     MedCategoryListCreateView,
#     CategoryListCreateView,
#     MedicineListCreateView,
#     MedicineDetailView
# )

# urlpatterns = [
#     path('medcategories/', MedCategoryListCreateView.as_view(), name='medcategory-list-create'),
#     path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
#     path('medicines/', MedicineListCreateView.as_view(), name='medicine-list-create'),
#     path('medicines/<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),
# ]


from django.urls import path
from .views import (
    CategoryListCreateView,
    MedicineListCreateView,
    InventoryListCreateView,
    InventoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("medicines/", MedicineListCreateView.as_view(), name="medicine-list-create"),
    path(
        "inventory/",
        InventoryListCreateView.as_view(),
        name="inventory-list-create",
    ),
    path(
        "inventory/<uuid:uid>/",
        InventoryRetrieveUpdateDestroyView.as_view(),
        name="inventory-retrieve-update-destroy",
    ),
]
