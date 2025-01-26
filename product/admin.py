from django.contrib import admin
from .models import Medicine, Category, Inventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["uid", "name", "description"]
    search_fields = ["name"]


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ["uid", "name", "generic_name", "manufacturer"]
    search_fields = ["name", "generic_name", "manufacturer"]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["uid", "medicine", "category", "stock", "price", "expiry_date"]
    list_filter = ["category", "expiry_date"]
    search_fields = ["medicine__name", "category__name"]
