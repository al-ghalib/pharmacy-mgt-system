from django.db import models
from base.models import BaseModel
from account.models import User
from product.models import Inventory


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.price_per_item:
            self.price_per_item = self.inventory.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.inventory.medicine.name} in {self.cart.user.email}'s cart"


ORDER_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

PAYMENT_METHOD_CHOICES = [
    ("cash", "Cash"),
    ("card", "Card"),
    ("online", "Online Payment"),
]


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)

    def calculate_total_price(self):
        """ Recalculate total price from OrderDetails """
        self.total_price = sum(detail.price for detail in self.order_details.all())
        self.save()

    def __str__(self):
        return f"Order {self.uid} by {self.user.email}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_details")
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="order_details")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Auto-fill price and quantity from CartItem before saving """
        if not self.pk: 
            self.price = self.cart_item.price_per_item
            self.quantity = self.cart_item.quantity

        super().save(*args, **kwargs)  

    def __str__(self):
        return f"OrderDetail {self.pk} for Order {self.order.uid}"



# first_name = models.CharField(max_length=100, blank=True, null=True)
# last_name = models.CharField(max_length=100, blank=True, null=True)