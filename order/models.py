from django.conf import settings
from django.db import models
from base.models import BaseModel
from product.models import Inventory


class Cart(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "inventory")

    def __str__(self):
        return f"{self.inventory.medicine.name} x{self.quantity}"


class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="order")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.uid} by {self.user.username}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="order_details"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.inventory.medicine.name} x{self.quantity}"
