from django.db import models
from base.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey(
        "account.User", 
        on_delete=models.CASCADE, 
        related_name="carts"
    )
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Cart {self.uid} for {self.user.email}"


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name="cart_items"
    )
    inventory = models.ForeignKey(
        "product.Inventory", 
        on_delete=models.CASCADE, 
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.quantity} of {self.inventory.medicine.name} in Cart {self.cart.uid}"


ORDER_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

PAYMENT_METHOD_CHOICES = [
    ("cash", "Cash"),
    ("card", "Card"),
    ("online", "Online Payment"),
]


class Order(BaseModel):
    user = models.ForeignKey(
        "account.User", 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default="pending"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )  
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, 
        choices=PAYMENT_METHOD_CHOICES, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"Order {self.uid} by {self.user.email}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="order_details"
    )
    cart_item = models.ForeignKey(
        CartItem, 
        on_delete=models.CASCADE, 
        related_name="order_details"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    ) 

    def __str__(self):
        return f"OrderDetail {self.id} for Order {self.order.uid}"
