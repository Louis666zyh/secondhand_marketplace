from django.db import models
from django.conf import settings
from apps.users.models import User


class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=255, unique=True, help_text="Name of the category.")

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model representing a product available on the platform."""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    name = models.CharField(max_length=255, help_text="Name of the product.")
    description = models.TextField(help_text="Description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product.")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text="Current status of the product."
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products",
        help_text="Category of the product."
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products",
        help_text="User who is selling the product."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the product was created.")
    is_approved = models.BooleanField(default=False, help_text="Indicates whether the product is approved by an admin.")

    def __str__(self):
        return f"{self.name} - {self.status}"
