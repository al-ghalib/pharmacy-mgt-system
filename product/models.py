from django.db import models
from base.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    generic_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Inventory(BaseModel):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="details")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="details")
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="Product_image/", blank=True, null=True)
    expiry_date = models.DateField()

    class Meta:
        unique_together = ('medicine', 'category')  

    def __str__(self):
        return f"{self.medicine} - {self.stock} units available"
    