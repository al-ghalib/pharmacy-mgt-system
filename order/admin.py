from django.contrib import admin
from .models import Cart, CartItem, Order, OrderDetail


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("uid", "user__email")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("uid", "cart", "inventory", "quantity", "price_per_item", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("uid", "cart__uid", "inventory__medicine__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "status", "total_price", "is_paid", "payment_method", "created_at", "updated_at")
    list_filter = ("status", "is_paid", "payment_method", "created_at")
    search_fields = ("uid", "user__email")


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("uid", "order", "cart_item", "quantity", "price", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("uid", "order__uid", "cart_item__inventory__medicine__name")
