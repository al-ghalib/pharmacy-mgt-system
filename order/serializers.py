from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderDetail
from product.models import Inventory


class CartItemSerializer(serializers.ModelSerializer):
    inventory = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["uid", "inventory", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.inventory.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["uid", "user", "created_at", "items"]


class OrderDetailSerializer(serializers.ModelSerializer):
    inventory = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = ["uid", "inventory", "quantity", "price", "total_price"]

    def get_total_price(self, obj):
        return obj.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    cart = CartSerializer()
    details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["uid", "user", "cart", "total_amount", "status", "placed_at", "details"]
