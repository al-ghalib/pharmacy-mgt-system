from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import BaseUserManager


class RoleChoices(models.TextChoices):
    ADMIN = "admin", "Admin"
    SALES = "sales", "Sales Associate"
    STOCK_UPDATER = "stock_updater", "Stock Updater"
    CUSTOMER = "customer", "Customer"


class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class StatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    REMOVED = "removed", "Removed"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("role") != "admin":
            raise ValueError("Superuser must have role of Admin")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
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
    image = models.ImageField(upload_to="user_images/", blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )
    role = models.CharField(
        max_length=20, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role == "admin"

    def is_active_status(self):
        return self.status == "active"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None


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
        User,
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

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"

    def is_active_member(self):
        return self.status == "active"


