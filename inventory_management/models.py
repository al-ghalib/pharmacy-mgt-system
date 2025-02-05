from django.db import models
from base.models import BaseModel
from product.models import Inventory
from account.models import User


class StockMovement(BaseModel):
    MOVEMENT_TYPES = [
        ("purchase", "Purchase"),
        ("sale", "Sale"),
        ("return", "Return"),
    ]

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="stock_movements")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    previous_stock = models.PositiveIntegerField()
    new_stock = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="stock_movements")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.previous_stock = self.inventory.stock
            if self.movement_type in ["purchase", "return"]:
                self.new_stock = self.previous_stock + self.quantity
            else:
                self.new_stock = self.previous_stock - self.quantity
            self.inventory.stock = self.new_stock
            self.inventory.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory.medicine.name} - {self.movement_type} ({self.quantity})"


class SalesRecord(BaseModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="sales_records")
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sales")
    date_sold = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_revenue = self.quantity_sold * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory.medicine.name} - {self.quantity_sold} units sold"


class MonthlySalesReport(BaseModel):
    month = models.DateField(unique=True)
    total_sales = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sales Report - {self.month.strftime('%B %Y')}"