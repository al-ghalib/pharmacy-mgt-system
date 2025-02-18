from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderDetail, CustomUser, Inventory
from account.models import Organization
from .models import OrderStatusChoices

# from product.serializers import InventorySerializer
from product.models import Medicine, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
        ]
        read_only_fields = ["id", "name"]


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

    def validate(self, data):
        inventory = data.get("inventory")
        quantity = data.get("quantity")

        try:
            inventory.refresh_from_db()
        except Inventory.DoesNotExist:
            raise serializers.ValidationError({"inventory": "Invalid inventory ID."})

        if quantity > inventory.stock:
            raise serializers.ValidationError(
                {
                    "quantity": f"Requested quantity ({quantity}) exceeds available stock ({inventory.stock})."
                }
            )

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

    def validate(self, data):
        is_paid = data.get("is_paid", False)
        payment_method = data.get("payment_method", None)
        status = data.get("status", OrderStatusChoices.PENDING)

        user = self.context["request"].user

        if self.instance and self.instance.status == OrderStatusChoices.CONFIRMED:
            raise serializers.ValidationError(
                {"status": "A confirmed order cannot be changed."}
            )

        if self.instance and self.instance.status == OrderStatusChoices.CONFIRMED:
            raise serializers.ValidationError(
                {"status": ["A confirmed order cannot be changed."]}
            )

        if status == OrderStatusChoices.CONFIRMED:
            if not is_paid:
                raise serializers.ValidationError(
                    {"is_paid": ["Order must be paid before confirmation."]}
                )
            if not payment_method:
                raise serializers.ValidationError(
                    {
                        "payment_method": [
                            "Payment method is required before confirmation."
                        ]
                    }
                )

        elif status == OrderStatusChoices.PENDING:
            if is_paid:
                raise serializers.ValidationError(
                    {"is_paid": ["A pending order cannot be marked as paid."]}
                )
            if payment_method:
                raise serializers.ValidationError(
                    {
                        "payment_method": [
                            "A pending order cannot have a payment method set."
                        ]
                    }
                )

        elif status == OrderStatusChoices.CANCELLED:
            if self.instance and self.instance.status == OrderStatusChoices.CONFIRMED:
                raise serializers.ValidationError(
                    {"status": ["A confirmed order cannot be cancelled."]}
                )

        cart = getattr(user, "carts", None)
        if not cart or not cart.cart_items.exists():
            raise serializers.ValidationError(
                {"cart": ["Cart is empty. Add Items first."]}
            )

        return data


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        read_only_fields = ["name"]


class MedicineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["name"]
        read_only_fields = ["name"]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name"]
        read_only_fields = ["name"]


class InventorySerializer(serializers.ModelSerializer):
    medicine = MedicineDetailSerializer(read_only=True)
    category = CategoryDetailSerializer(read_only=True)
    organization = OrganizationDetailSerializer(read_only=True)

    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), write_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "medicine",
            "medicine_id",
            "category",
            "category_id",
            "organization",
            "organization_id",
            "price",
        ]
        read_only_fields = ["id", "uid"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    inventory = InventorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = [
            "id",
            "uid",
            "order",
            "inventory",
            "quantity",
            "total_price",
            "user",
            "organization",
        ]
        read_only_fields = [
            "id",
            "uid",
            "order",
            "inventory",
            "quantity",
            "user",
            "organization",
        ]

    def get_total_price(self, obj):
        return str(obj.quantity * obj.price)
