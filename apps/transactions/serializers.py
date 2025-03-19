from rest_framework import serializers
from .models import Transaction
from apps.products.serializers import ProductSerializer, UserSerializer
from ..reviews.models import Review


class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    order_serial = serializers.CharField(read_only=True)
    reviewed = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'product', 'product_id', 'buyer', 'seller', 'status', 'order_serial', 'payment_method',
            'payment_date',
            'transaction_reference', 'shipping_address', 'cancellation_reason', 'total_price', 'created_at',
            'delivery_method', 'return_status', 'reviewed'
        ]

    def get_reviewed(self, obj):
        # 检查该交易是否已有评价
        return Review.objects.filter(transaction=obj).exists()

    def validate(self, data):
        if not data.get('product_id'):
            raise serializers.ValidationError({"product_id": "Product ID is required."})
        return data

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        validated_data.pop('product', None)  # Remove read-only field
        transaction = Transaction.objects.create(**validated_data, product_id=product_id)
        return transaction
