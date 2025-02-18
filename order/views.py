from rest_framework import generics, status
from account.permissions import IsSalesAssociate, IsOrganizationAdmin
from .models import Cart, CartItem, Order, OrderDetail
from account.models import RoleChoices, OrganizationUser
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderDetailsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        order = serializer.save(user=self.request.user)
        order.calculate_total_price()

        if order.is_paid and order.payment_method:
            order.confirm_order()


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

    # def get_queryset(self):
    #     user = self.request.user

    #     try:
    #         organization_user = user.organization_memberships.first() 
    #     except OrganizationUser.DoesNotExist:
    #         return OrderDetail.objects.none()

    #     if organization_user.role in [RoleChoices.SALES, RoleChoices.ADMIN]:
    #         return OrderDetail.objects.filter(
    #             order__user__organization_memberships__organization=organization_user.organization
    #         )
    #     else:
    #         return OrderDetail.objects.none()