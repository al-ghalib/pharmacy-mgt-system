from rest_framework import generics, status
from account.permissions import IsSalesAssociate, IsOrganizationAdmin
from .models import Cart, CartItem, Order, OrderDetail
# from account.models import RoleChoices, OrganizationUser
from .models import OrderStatusChoices
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderDetailsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from django.db import transaction
from django.core.exceptions import ValidationError



class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uid"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemListCreateView(generics.ListCreateAPIView):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Cart is empty"}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            
            order = serializer.save(user=self.request.user)
            
            order.calculate_total_price()

            if order.status == OrderStatusChoices.CONFIRMED:
                order.confirm_order()

            return Response(
                {"message": "Order has been created successfully!", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            error_details = e.detail if hasattr(e, 'detail') else {"error": e.messages}
            return Response({"error": error_details}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uid"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailsListView(generics.ListAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsOrganizationAdmin | IsSalesAssociate]

