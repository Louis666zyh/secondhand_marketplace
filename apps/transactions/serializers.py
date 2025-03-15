from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source="buyer.username")

    class Meta:
        model = Transaction
        fields = ["id", "product", "buyer", "status", "payment_method", "payment_date", "total_price",
                  "transaction_reference", "shipping_address", "cancellation_reason", "created_at"]
        extra_kwargs = {
            "buyer": {"read_only": True},
            "total_price": {"read_only": True},
        }
