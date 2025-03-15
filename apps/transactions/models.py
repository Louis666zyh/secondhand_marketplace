from django.db import models
from apps.products.models import Product
from apps.users.models import User

class Transaction(models.Model):
    """
    Model representing a transaction on the platform.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                help_text="Product involved in the transaction.")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions",
                              help_text="User who purchased the product.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',
                              help_text="Status of the transaction.")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True,
                                      help_text="Payment method used by the buyer.")
    payment_date = models.DateTimeField(blank=True, null=True, help_text="Date and time when the payment was completed.")
    transaction_reference = models.CharField(max_length=255, blank=True, null=True,
                                             help_text="Reference number provided by the third-party payment gateway.")
    shipping_address = models.TextField(blank=True, null=True,
                                        help_text="Shipping address for the product.")
    cancellation_reason = models.TextField(blank=True, null=True,
                                           help_text="Reason for transaction cancellation, if applicable.")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                      help_text="Total price of the transaction.")
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="Date and time when the transaction was created.")

    def save(self, *args, **kwargs):
        """Automatically calculate total price"""
        if self.product:
            self.total_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction #{self.id} - {self.status}"
