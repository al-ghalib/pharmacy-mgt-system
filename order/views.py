from rest_framework import generics
from account.permissions import IsCustomer, IsSalesAssociate
from .models import Cart, CartItem, Order, OrderDetail
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderDetailsSerializer,
)

# class CartListCreateView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsCustomer]

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]  

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    lookup_field = "uid"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        order.calculate_total_price()

        if order.is_paid and order.payment_method:
            order.confirm_order()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]
    lookup_field = "uid"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailsListView(generics.ListAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsSalesAssociate] 
