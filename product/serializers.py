from rest_framework import serializers
from .models import Medicine, Category, Inventory, Organization
from account.models import OrganizationUser, StatusChoices


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "uid", "name", "description"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "uid", "name", "generic_name", "description", "manufacturer"]


class MedicineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class InventorySerializer(serializers.ModelSerializer):
    medicine = MedicineDetailSerializer(read_only=True)
    category = CategoryDetailSerializer(read_only=True)
    organization = OrganizationDetailSerializer(read_only=True)

    medicine_id = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), write_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "uid",
            "medicine",
            "medicine_id",
            "category",
            "category_id",
            "organization",
            "organization_id",
            "stock",
            "price",
            "image",
            "expiry_date",
        ]
        read_only_fields = ["id", "uid"]


    def validate_organization_id(self, organization):
        user = self.context["request"].user
        if not OrganizationUser.objects.filter(user=user, organization=organization, status=StatusChoices.ACTIVE).exists():
            raise serializers.ValidationError("You do not have permission to manage inventory for this organization.")
        return organization
    

    def create(self, validated_data):
        medicine = validated_data.pop("medicine_id")
        category = validated_data.pop("category_id")
        organization = validated_data.pop("organization_id")

        user = self.context["request"].user
        if not OrganizationUser.objects.filter(user=user, organization=organization, status=StatusChoices.ACTIVE).exists():
            raise serializers.ValidationError(
                {"detail": "You do not have permission to create inventory for this organization."}
            )

        if Inventory.objects.filter(medicine=medicine, category=category, organization=organization).exists():
            raise serializers.ValidationError(
                {"detail": "This inventory already exists for this organization."}
            )

        return Inventory.objects.create(medicine=medicine, category=category, organization=organization, **validated_data)


# class InventoryStockUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Inventory
#         fields = ["stock"]

#     def validate_stock(self, value):
#         if value < 0:
#             raise serializers.ValidationError("Stock cannot be negative.")
#         return value


#     def update(self, instance, validated_data):
#         user = self.context["request"].user

#         if not OrganizationUser.objects.filter(user=user, organization=instance.organization, status=StatusChoices.ACTIVE).exists():
#             raise serializers.ValidationError(
#                 {"detail": "You do not have permission to update this inventory."}
#             )

#         return super().update(instance, validated_data)

class InventoryStockUpdateSerializer(serializers.ModelSerializer):
    increase = serializers.IntegerField(required=False, min_value=1)
    decrease = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = Inventory
        fields = ["increase", "decrease"]

    def validate(self, data):
        if not (data.get("increase") or data.get("decrease")):
            raise serializers.ValidationError("You must provide either 'increase' or 'decrease'.")
        if data.get("increase") and data.get("decrease"):
            raise serializers.ValidationError("You cannot provide both 'increase' and 'decrease'.")
        return data

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if not OrganizationUser.objects.filter(user=user, organization=instance.organization, status=StatusChoices.ACTIVE).exists():
            raise serializers.ValidationError(
                {"detail": "You do not have permission to update this inventory."}
            )
        increase = validated_data.get("increase", 0)
        decrease = validated_data.get("decrease", 0)

        if increase:
            instance.stock += increase
            msg = f"Stock increased by {increase}."
        elif decrease:
            if instance.stock - decrease < 0:
                raise serializers.ValidationError("Stock cannot be negative after decrease.")
            instance.stock -= decrease
            msg = f"Stock decreased by {decrease}."

        instance.save()
        return instance, msg