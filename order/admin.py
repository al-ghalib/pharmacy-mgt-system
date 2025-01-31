from django.contrib import admin
from .models import Cart, CartItem, Order, OrderDetail


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "inventory", "quantity", "price_per_item")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "total_price", "is_paid", "created_at")


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("order", "cart_item", "quantity", "price")
