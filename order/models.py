from django.db import models, transaction
from base.models import BaseModel
from account.models import User
from product.models import Inventory

class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethodChoices(models.TextChoices):
    CASH = "cash", "Cash"
    CARD = "card", "Card"
    ONLINE = "online", "Online Payment"


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carts")
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
        if not self.price_per_item:
            self.price_per_item = self.inventory.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.inventory.medicine.name} in {self.cart.user.email}'s cart"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
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
        cart = self.user.carts

        cart_items = cart.cart_items.all()
     
        self.total_price = sum(
            cart_item.price_per_item * cart_item.quantity for cart_item in cart_items
        )
        self.save()


    def confirm_order(self):
        if self.status == OrderStatusChoices.PENDING:
            if not self.is_paid:
                raise ValueError(
                    "Order cannot be confirmed until payment is completed."
                )
            if not self.payment_method:
                raise ValueError(
                    "Payment method must be selected before confirming the order."
                )

            with transaction.atomic():
                cart = self.user.carts

                cart_items = cart.cart_items.all()

                if not cart_items:
                    raise ValueError(
                        "Cart is empty. Cannot confirm an order with no items."
                    )

                for cart_item in cart_items:
                    OrderDetail.objects.create(
                        order=self,
                        cart_item=cart_item,
                        quantity=cart_item.quantity,
                        price=cart_item.price_per_item,
                    )

                self.calculate_total_price()
                
                self.status = OrderStatusChoices.CONFIRMED
                self.save()


    def __str__(self):
        return f"Order {self.uid} by {self.user.email}"



class OrderDetail(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_details"
    )
    cart_item = models.ForeignKey(
        CartItem, on_delete=models.CASCADE, related_name="order_details"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.cart_item.price_per_item
            self.quantity = self.cart_item.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetail {self.pk} for Order {self.order.uid}"




 # def calculate_total_price(self):
    #     try:
    #         cart = self.user.carts
    #         cart_items = cart.cart_items.all()

    #         self.total_price = sum(
    #             cart_item.price_per_item * cart_item.quantity for cart_item in cart_items
    #         )
    #         self.save()
    #     except ObjectDoesNotExist:
    #         raise ValueError("User does not have an active cart.")


    # def calculate_total_price(self):
    #     cart = self.user.carts
    #     # if not cart.is_active:
    #     #     raise ValueError("User does not have an active cart.")

    #     cart_items = cart.cart_items.all()
    #     # if not cart_items:
    #     #     raise ValueError("Cart is empty. Cannot calculate total price for an empty cart.")

    #     self.total_price = sum(
    #         cart_item.price_per_item * cart_item.quantity for cart_item in cart_items
    #     )
    #     self.save()
        
    # def calculate_total_price(self):
    #     order_details = self.order_details.all()
    #     # if not order_details:
    #     #     raise ValueError("Order details are empty. Cannot calculate total price.")

    #     self.total_price = sum(
    #         order_detail.price * order_detail.quantity for order_detail in order_details
    #     )
    #     self.save()


    # def confirm_order(self):
    #     if self.status == OrderStatusChoices.PENDING:
    #         if not self.is_paid:
    #             raise ValueError(
    #                 "Order cannot be confirmed until payment is completed."
    #             )
    #         if not self.payment_method:
    #             raise ValueError(
    #                 "Payment method must be selected before confirming the order."
    #             )

    #         with transaction.atomic():
    #             cart = self.user.carts
    #             # if not cart or not cart.is_active:
    #             #     raise ValueError("User does not have an active cart.")

    #             cart_items = cart.cart_items.all()
                
    #             # if not cart_items:
    #             #     raise ValueError(
    #             #         "Cart is empty. Cannot confirm an order with no items."
    #             #     )

    #             for cart_item in cart_items:
    #                 OrderDetail.objects.create(
    #                     order=self,
    #                     cart_item=cart_item,
    #                     quantity=cart_item.quantity,
    #                     price=cart_item.price_per_item,
    #                 )

    #             # cart_items.delete()
    #             # cart.cart_items.all().delete()
    #             self.calculate_total_price()
    #             self.status = OrderStatusChoices.CONFIRMED
    #             self.save()

    # def confirm_order(self):
    #     if self.status == OrderStatusChoices.PENDING:
    #         if not self.is_paid:
    #             raise ValueError("Order cannot be confirmed until payment is completed.")
    #         if not self.payment_method:
    #             raise ValueError("Payment method must be selected before confirming the order.")

    #         with transaction.atomic():
    #             cart = self.user.carts
    #             cart_items = cart.cart_items.all()

    #             if not cart_items:
    #                 raise ValueError("Cart is empty. Cannot confirm an order with no items.")

    #             total_price = sum(
    #                 cart_item.price_per_item * cart_item.quantity for cart_item in cart_items
    #             )

    #             for cart_item in cart_items:
    #                 OrderDetail.objects.create(
    #                     order=self,
    #                     cart_item=cart_item,
    #                     quantity=cart_item.quantity,
    #                     price=cart_item.price_per_item,
    #                 )

    #             self.total_price = total_price
    #             self.status = OrderStatusChoices.CONFIRMED
    #             self.save()