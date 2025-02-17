from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderDetail, CustomUser, Inventory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "uid", "user", "is_active", "created_at", "updated_at"]
        read_only_fields = ["uid", "user", "created_at", "updated_at"]

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            is_active = data.get("is_active", True)

            # if is_active and Cart.objects.filter(user=user, is_active=True).exists():
            #     raise serializers.ValidationError({"errors": "User can only have one active cart."})
            if is_active and Cart.objects.filter(user=user, is_active=True).exists():
                raise serializers.ValidationError("User can only have one active cart.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    inventory = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(), write_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["inventory"] = {
            "id": instance.inventory.id,
            "medicine_name": instance.inventory.medicine.name,
            "stock": instance.inventory.stock,
        }
        return data

    class Meta:
        model = CartItem
        fields = [
            "id",
            "uid",
            "cart",
            "inventory",
            "quantity",
            "price_per_item",
        ]
        read_only_fields = ["uid", "price_per_item"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "uid",
            "user",
            "status",
            "total_price",
            "is_paid",
            "payment_method",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "total_price", "created_at", "updated_at"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    cart_item = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderDetail
        fields = ["id", "uid", "order", "cart_item", "quantity", "price"]
        read_only_fields = ["id", "uid", "order", "cart_item", "quantity", "price"]
