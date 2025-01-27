from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from base.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender_choices = [("male", "Male"), ("female", "Female"), ("other", "Other")]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    status_choices = [("active", "Active"), ("inactive", "Inactive"), ("removed", "Removed")]
    status = models.CharField(max_length=10, choices=status_choices, default="active")

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Organization(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=False, null=True)  
    email = models.EmailField(blank=False, null=True)  
    address = models.TextField(blank=False, null=True)  
    trade_licence = models.CharField(max_length=100, blank=False, null=True)  
    details = models.TextField(blank=True, null=True)  
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class OrganizationUser(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="organization_users",
    )
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("sales", "Sales Associate"),
        ("stock_updater", "Stock Updater"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales")
    status_choices = [("active", "Active"), ("inactive", "Inactive"), ("removed", "Removed")]
    status = models.CharField(max_length=10, choices=status_choices, default="active")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"



# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     organization = models.ForeignKey(
#         "Organization",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="users",
#     )

#     ROLE_CHOICES = [
#         ("admin", "Admin"),
#         ("sales", "Sales Associate"),
#         ("stock_updater", "Stock Updater"),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales")

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def __str__(self):
#         return self.email


# class Organization(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class OrganizationUser(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="organization_memberships"
#     )
#     organization = models.ForeignKey(
#         Organization, on_delete=models.CASCADE, related_name="organization_users"
#     )
#     is_admin = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.email} - {self.organization.name}"
