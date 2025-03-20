from django.db import models
from apps.products.models import Product
from apps.users.models import User


class Transaction(models.Model):
    """
    Model for transactions on the platform.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('received', 'Received'),  # New status for buyer confirmation
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    DELIVERY_METHOD_CHOICES = [
        ('face-to-face', 'Face-to-Face'),
        ('shipping', 'Shipping'),
    ]
    RETURN_STATUS_CHOICES = [
        ('none', 'None'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                help_text="The product involved in the transaction.")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_transactions",
                              help_text="The user who purchased the product.")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_transactions",
                               help_text="The user who sold the product.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',
                              help_text="The status of the transaction.")
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, blank=True, null=True,
                                       help_text="The chosen delivery method.")
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='none',
                                     help_text="The status of the return request.")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True,
                                      help_text="The payment method used by the buyer.")
    payment_date = models.DateTimeField(blank=True, null=True, help_text="The time when the payment was completed.")
    transaction_reference = models.CharField(max_length=255, blank=True, null=True,
                                             help_text="The reference number provided by the payment gateway.")
    shipping_address = models.TextField(blank=True, null=True,
                                        help_text="The delivery address for the product.")
    cancellation_reason = models.TextField(blank=True, null=True,
                                           help_text="The reason for cancellation (if applicable).")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                      help_text="The total price of the transaction.")
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="The date and time when the transaction was created.")
    order_serial = models.CharField(max_length=50, blank=True, null=True, help_text="Unique order serial number.")

    def save(self, *args, **kwargs):
        """Automatically calculate the total price and set the seller."""
        if self.product:
            self.total_price = self.product.price
            self.seller = self.product.seller  # Set the seller from the product
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction #{self.id} - {self.status}"