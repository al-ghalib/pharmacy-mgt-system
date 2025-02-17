from rest_framework import generics
from account.permissions import IsSalesAssociate
from .models import Medicine, Category, Inventory
from .serializers import (
    MedicineSerializer,
    CategorySerializer,
    InventorySerializer,
)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSalesAssociate]


class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsSalesAssociate]


class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsSalesAssociate]


class InventoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsSalesAssociate]
    lookup_field = "uid"
