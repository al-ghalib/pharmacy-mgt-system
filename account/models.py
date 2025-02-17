from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import BaseModel
from .managers import UserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    SALES = "SALES", "Sales Associate"
    STOCK_UPDATER = "STOCK_UPDATER", "Stock Updater"
    CUSTOMER = "CUSTOMER", "Customer"


class GenderChoices(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


class StatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    REMOVED = "REMOVED", "Removed"



class CustomUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, blank=True, null=True
    )
    image = models.ImageField(upload_to="User_images/", blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_active_status(self):
        return self.status == StatusChoices.ACTIVE

    def get_image_url(self):
        return self.image.url if self.image else None


class Organization(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    trade_licence = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)

    def __str__(self):
        return self.name


class OrganizationUser(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="organization_users",
    )

    role = models.CharField(
        max_length=20, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER
    ) 

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )

    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"], name="unique_user_organization"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"

    def is_active_member(self):
        return self.status == StatusChoices.ACTIVE
    
    
    def save(self, *args, **kwargs):
        if self.salary and self.salary < 0:
            raise ValueError("Salary cannot be negative.")
        super().save(*args, **kwargs)
 


