from django.contrib import admin
from .models import Cart, CartItem, Order, OrderDetail


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "created_at")
    search_fields = ("user__username",)
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "status", "total_amount", "placed_at")
    list_filter = ("status",)
    search_fields = ("user__username",)
    inlines = [OrderDetailInline]


admin.site.register(Order, OrderAdmin)


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("uid", "order", "inventory", "quantity", "price")
    search_fields = ("order__uid", "inventory__medicine__name")


admin.site.register(OrderDetail, OrderDetailAdmin)


# from django.contrib import admin
# from .models import Order, OrderDetail, Cart, CartItem


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["order_id", "customer_name", "status", "created_at"]
#     search_fields = ["order_id", "customer_name", "customer_email"]
#     list_filter = ["status", "created_at"]


# @admin.register(OrderDetail)
# class OrderDetailAdmin(admin.ModelAdmin):
#     list_display = ["product_name", "quantity", "price", "total_price", "order"]
#     search_fields = ["product_name", "order__order_id"]


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ["id", "customer_name", "created_at"]
#     search_fields = ["customer_name", "customer_email"]


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ["product_name", "quantity", "price", "total_price", "cart"]
#     search_fields = ["product_name", "cart__id"]
