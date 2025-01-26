from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Medicine, Category, Inventory
from .serializers import (
    MedicineSerializer,
    CategorySerializer,
    InventorySerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InventoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = "uid"





# class InventoryListCreateView(generics.ListCreateAPIView):
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer

# class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer

# # Integration Logic for Cart
# def add_to_cart(cart, medicine_name, quantity):
#     try:
#         inventory_item = Inventory.objects.get(medicine_name=medicine_name)
#         if not inventory_item.check_availability(quantity):
#             raise ValidationError(f"Insufficient stock for {medicine_name}. Only {inventory_item.quantity_available} units available.")

#         CartItem.objects.create(cart=cart, product_name=medicine_name, quantity=quantity, price=0.0)  # Assuming price logic is handled elsewhere
#     except Inventory.DoesNotExist:
#         raise ValidationError(f"{medicine_name} is not available in inventory.")

# # Integration Logic for Order
# def process_order(order):
#     for detail in order.order_details.all():
#         inventory_item = Inventory.objects.get(medicine_name=detail.product_name)
#         inventory_item.reduce_quantity(detail.quantity)
