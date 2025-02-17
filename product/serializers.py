from rest_framework import serializers
from .models import Medicine, Category, Inventory


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



class InventorySerializer(serializers.ModelSerializer):
    medicine = MedicineDetailSerializer(read_only=True)
    category = CategoryDetailSerializer(read_only=True)

    medicine_id = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "uid",
            "medicine",
            "medicine_id",
            "category",
            "category_id",
            "stock",
            "price",
            "image",
            "expiry_date",
        ]
        read_only_fields = ["id", "uid"]


    def create(self, validated_data):
        medicine = validated_data.pop("medicine_id")
        category = validated_data.pop("category_id")

        if Inventory.objects.filter(medicine=medicine, category=category).exists():
            raise serializers.ValidationError(
                {"detail": "This inventory is already available."}
            )
        
        return Inventory.objects.create(medicine=medicine, category=category, **validated_data)