from rest_framework import serializers
from .models import Medicine, Category, Inventory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uid", "name", "description"]


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["uid", "name", "generic_name", "description", "manufacturer"]


class InventorySerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Inventory
        fields = [
            "uid",
            "medicine",
            "category",
            "stock",
            "price",
            "image",
            "expiry_date",
        ]
