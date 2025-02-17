from django.db import models, transaction
from base.models import BaseModel
from account.models import CustomUser
from product.models import Inventory


class OrderStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"


class PaymentMethodChoices(models.TextChoices):
    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"
    ONLINE = "ONLINE", "Online Payment"


class Cart(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="carts"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.price_per_item and self.inventory:
            self.price_per_item = self.inventory.price
        elif not self.inventory:
            raise ValueError("Inventory must be set before saving a CartItem.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.inventory.medicine.name} in {self.cart.user.email}'s cart"


class Order(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethodChoices.choices, blank=True, null=True
    )

    def calculate_total_price(self):
        cart = getattr(self.user, "carts", None)
        if not cart:
            self.total_price = 0
            return

        cart_items = cart.cart_items.all()
        self.total_price = sum(
            item.price_per_item * item.quantity for item in cart_items
        )
        self.save()

    def confirm_order(self):
        # if self.status != OrderStatusChoices.PENDING:
        #     raise ValueError("Only pending orders can be confirmed.")

        if not self.is_paid:
            raise ValueError("Order cannot be confirmed until payment is completed.")

        if not self.payment_method:
            raise ValueError(
                "Payment method must be selected before confirming the order."
            )

        with transaction.atomic():
            cart = self.user.carts

            if not cart:
                raise ValueError("Cart does not exist.")

            cart_items = cart.cart_items.all()
            if not cart_items:
                raise ValueError(
                    "Cart is empty. Cannot confirm an order with no items."
                )

            for cart_item in cart_items:
                if cart_item.inventory.stock < cart_item.quantity:
                    raise ValueError(
                        f"Not enough stock for {cart_item.inventory.medicine.name}. Available: {cart_item.inventory.stock}"
                    )
                cart_item.inventory.stock -= cart_item.quantity
                cart_item.inventory.save()

                OrderDetail.objects.create(
                    order=self,
                    inventory=cart_item.inventory,
                    quantity=cart_item.quantity,
                    price=cart_item.price_per_item,
                )

            self.calculate_total_price()

            self.status = OrderStatusChoices.CONFIRMED
            self.save()

            cart.cart_items.all().delete()

    def __str__(self):
        return f"Order {self.uid} by {self.user.email}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_details"
    )
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="order_details"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.inventory.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetail {self.pk} for Order {self.order.uid}"
