from django.db import models
from apps.products.models import Product
from apps.users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model representing a product review.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews',
                                help_text="Product that is being reviewed.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews',
                             help_text="User who wrote the review.")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating given by the user (1-5)."
    )
    comment = models.TextField(help_text="Content of the review.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the review was created.")

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
