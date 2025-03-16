from rest_framework import serializers
from apps.users.models import User
from apps.products.models import Product
from apps.transactions.models import Transaction

class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin user approval."""
    class Meta:
        model = User
        fields = ["id", "username", "is_approved"]
        extra_kwargs = {"is_approved": {"required": True}}

class AdminProductSerializer(serializers.ModelSerializer):
    """Serializer for product approval by admin."""
    class Meta:
        model = Product
        fields = ["id", "name", "is_approved", "image"]
        extra_kwargs = {"is_approved": {"required": True}}

class AdminTransactionSerializer(serializers.ModelSerializer):
    """Serializer for updating transaction status."""
    class Meta:
        model = Transaction
        fields = ["id", "status"]
        extra_kwargs = {"status": {"required": True}}
