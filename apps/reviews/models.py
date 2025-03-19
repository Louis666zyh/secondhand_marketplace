# apps/reviews/models.py
from django.db import models
from apps.transactions.models import Transaction  # 引入 Transaction 模型
from apps.users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE, related_name='reviews',
                                    help_text="Transaction associated with this review.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', db_index=True,
                             help_text="User who wrote the review (buyer).")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating given by the user (1-5)."
    )
    comment = models.TextField(help_text="Content of the review.")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      help_text="Date and time when the review was created.")
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes for the review.")

    def __str__(self):
        return f"Review for Transaction #{self.transaction.id} by {self.user.username}"

    class Meta:
        unique_together = ['transaction', 'user']  # 确保一个用户对一个交易只能评价一次

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images', db_index=True,
                               help_text="Review associated with this image.")
    image = models.ImageField(upload_to="review_images/%Y/%m/%d/", help_text="Image attached to the review.")

    def __str__(self):
        return f"Image for review {self.review.id}"