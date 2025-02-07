from django.db import models
from django.db.models import F, Sum
from base.models import BaseModel
from product.models import Inventory
from account.models import User
from django.core.exceptions import ValidationError


class MovementTypeChoices(models.TextChoices):
    PURCHASE = "purchase", "Purchase"
    SALE = "sale", "Sale"
    RETURN = "return", "Return"


class StockMovement(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="stock_movements"
    )
    movement_type = models.CharField(max_length=20, choices=MovementTypeChoices.choices)
    quantity = models.PositiveIntegerField()
    previous_stock = models.PositiveIntegerField(editable=False)
    new_stock = models.PositiveIntegerField(editable=False)
    notes = models.TextField(blank=True, null=True)
    handled_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="stock_movements"
    )

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.previous_stock = self.inventory.stock
            if self.movement_type in ["purchase", "return"]:
                self.new_stock = self.previous_stock + self.quantity
            elif self.movement_type == "sale":
                if self.quantity > self.previous_stock:
                    raise ValidationError("Not enough stock for this sale.")
                self.new_stock = self.previous_stock - self.quantity
            
            Inventory.objects.filter(id=self.inventory.id).update(stock=F("stock") + (self.quantity if self.movement_type in ["purchase", "return"] else -self.quantity))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory.medicine.name} - {self.movement_type} ({self.quantity})"


class SalesRecord(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="sales_records"
    )
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    sold_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sales"
    )
    date_sold = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity_sold > self.inventory.stock:
            raise ValidationError("Not enough stock available for this sale.")

        self.total_revenue = self.quantity_sold * self.unit_price

        StockMovement.objects.create(
            inventory=self.inventory,
            movement_type=MovementTypeChoices.SALE,
            quantity=self.quantity_sold,
            handled_by=self.sold_by,
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory.medicine.name} - {self.quantity_sold} units sold"


class MonthlySalesReport(BaseModel):
    month = models.DateField(unique=True)
    total_sales = models.PositiveIntegerField(default=0, editable=False)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)

    def save(self, *args, **kwargs):
        sales_data = SalesRecord.objects.filter(date_sold__year=self.month.year, date_sold__month=self.month.month).aggregate(
            total_sales=Sum("quantity_sold"),
            total_revenue=Sum("total_revenue"),
        )

        self.total_sales = sales_data["total_sales"] or 0
        self.total_revenue = sales_data["total_revenue"] or 0.00
        self.month = self.month.replace(day=1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sales Report of - {self.month.strftime('%B %Y')}"


# from django.db import models
# from base.models import BaseModel
# from product.models import Inventory
# from account.models import User


# class MovementTypeChoices(models.TextChoices):
#     PURCHASE = "purchase", "Purchase"
#     SALE = "sale", "Sale"
#     RETURN = "return", "Return"


# class StockMovement(BaseModel):
#     inventory = models.ForeignKey(
#         Inventory, on_delete=models.CASCADE, related_name="stock_movements"
#     )
#     movement_type = models.CharField(max_length=20, choices=MovementTypeChoices.choices)
#     quantity = models.PositiveIntegerField()
#     previous_stock = models.PositiveIntegerField()
#     new_stock = models.PositiveIntegerField()
#     notes = models.TextField(blank=True, null=True)
#     handled_by = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="stock_movements"
#     )

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.previous_stock = self.inventory.stock
#             if self.movement_type in ["purchase", "return"]:
#                 self.new_stock = self.previous_stock + self.quantity
#             else:
#                 self.new_stock = self.previous_stock - self.quantity
#             self.inventory.stock = self.new_stock
#             self.inventory.save()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return (
#             f"{self.inventory.medicine.name} - {self.movement_type} ({self.quantity})"
#         )


# class SalesRecord(BaseModel):
#     inventory = models.ForeignKey(
#         Inventory, on_delete=models.CASCADE, related_name="sales_records"
#     )
#     quantity_sold = models.PositiveIntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_revenue = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
#     sold_by = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="sales"
#     )
#     date_sold = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         self.total_revenue = self.quantity_sold * self.unit_price
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.inventory.medicine.name} - {self.quantity_sold} units sold"


# class MonthlySalesReport(BaseModel):
#     month = models.DateField(unique=True)
#     total_sales = models.PositiveIntegerField(default=0)
#     total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"Sales Report - {self.month.strftime('%B %Y')}"
