from rest_framework import generics, status
from account.permissions import IsSalesAssociate, IsStockUpdater
from .models import Medicine, Category, Inventory
from .serializers import (
    MedicineSerializer,
    CategorySerializer,
    InventorySerializer,
    InventoryStockUpdateSerializer,
)
from rest_framework.response import Response


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
    permission_classes = [IsSalesAssociate | IsStockUpdater]


class InventoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsSalesAssociate | IsStockUpdater]
    lookup_field = "uid"


# class InventoryStockUpdateView(generics.UpdateAPIView):
#     queryset = Inventory.objects.all()
#     serializer_class = InventoryStockUpdateSerializer
#     permission_classes = [IsStockUpdater]
#     lookup_field = "uid"

#     def perform_update(self, serializer):
#         inventory = serializer.instance
#         previous_stock = inventory.stock
#         updated_inventory = serializer.save()

#         print(f"Stock updated: {inventory.medicine} - {previous_stock} → {updated_inventory.stock}")

class InventoryStockUpdateView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryStockUpdateSerializer
    permission_classes = [IsStockUpdater]
    lookup_field = "uid"

    def perform_update(self, serializer):
        inventory = serializer.instance
        previous_stock = inventory.stock

        updated_inventory, msg = serializer.save()

        print(f"Stock updated: {inventory.medicine} - {previous_stock} → {updated_inventory.stock}")

        return updated_inventory, msg

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            updated_inventory, msg = self.perform_update(serializer)
            response_data = {
                "message": msg,
                # "updated_inventory": self.get_serializer(updated_inventory).data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)