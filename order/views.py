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



### Jhamela etay ###
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        order.calculate_total_price()




class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]
    lookup_field = "uid"

    # def get_queryset(self):
    #     return Order.objects.filter(user=self.request.user)


class OrderDetailsListView(generics.ListAPIView):
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsSalesAssociate] 

    def get_queryset(self):
        return OrderDetail.objects.filter(order__user=self.request.user)





# class OrderListCreateView(generics.ListCreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsCustomer]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         order = serializer.save(user=self.request.user)
        
#         cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
#         if not cart or not cart.cart_items.exists():
#             raise ValidationError("Cannot place an order with an empty or inactive cart.")
        
#         total_price = sum(
#             cart_item.price_per_item * cart_item.quantity for cart_item in cart.cart_items.all()
#         )

#         order.total_price = total_price
#         order.save()











# class OrderListCreateView(generics.ListCreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsCustomer]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         order = serializer.save(user=self.request.user)

#         cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
#         if not cart or not cart.cart_items.exists():
#             raise ValidationError("Cannot place an order with an empty or inactive cart.")

#         total_price = sum(
#             cart_item.price_per_item * cart_item.quantity for cart_item in cart.cart_items.all()
#         )
#         order.total_price = total_price
#         order.save()