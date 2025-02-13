from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderDetail, User, Inventory


# class CartSerializer(serializers.ModelSerializer):
#     class UserSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = User
#             fields = [
#                 "id",
#                 "email",
#             ]

#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Cart
#         fields = ["id", "uid", "user", "is_active", "created_at", "updated_at"]

#         read_only_fields = ["uid", "user", "created_at", "updated_at"]

#     def create(self, validated_data):
#         request = self.context.get("request")
#         if request and request.user.is_authenticated:
#             validated_data["user"] = request.user  
#         return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
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
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "email",
            ]

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
    class Meta:
        model = OrderDetail
        fields = ["id", "uid", "order", "cart_item", "quantity", "price"]
        read_only_fields = ["uid", "order", "cart_item", "quantity", "price"]



# class OrderSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), write_only=True
#     )  # Allow Admin/Sales Associate to specify user ID
#     order_details = OrderDetailSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = [
#             "id",
#             "uid",
#             "user",
#             "status",
#             "total_price",
#             "is_paid",
#             "payment_method",
#             "order_details",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["uid", "total_price", "order_details", "created_at", "updated_at"]

#     def create(self, validated_data):
#         user = validated_data.pop("user")  # Get user from request

#         # Fetch the user's active cart
#         try:
#             cart = Cart.objects.get(user=user, is_active=True)
#         except Cart.DoesNotExist:
#             raise serializers.ValidationError("User does not have an active cart.")

#         cart_items = cart.cart_items.all()
#         if not cart_items:
#             raise serializers.ValidationError("Cart is empty. Cannot create order.")

#         # Create the order
#         order = Order.objects.create(user=user, **validated_data)

#         # Create OrderDetail for each CartItem
#         order_details = []
#         for cart_item in cart_items:
#             order_details.append(
#                 OrderDetail(
#                     order=order,
#                     cart_item=cart_item,
#                     quantity=cart_item.quantity,
#                     price=cart_item.price_per_item,
#                 )
#             )

#         # Bulk create OrderDetails
#         OrderDetail.objects.bulk_create(order_details)

#         # Clear the cart
#         cart_items.delete()
#         cart.is_active = False
#         cart.save()

#         # Recalculate total price
#         order.calculate_total_price()

#         return order

