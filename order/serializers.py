from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderDetail


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["uid", "user", "is_active", "created_at", "updated_at"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["uid", "cart", "inventory", "quantity", "price_per_item", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["uid", "user", "status", "total_price", "is_paid", "payment_method", "created_at", "updated_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ["uid", "order", "cart_item", "quantity", "price", "created_at", "updated_at"]
