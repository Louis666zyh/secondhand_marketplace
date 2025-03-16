from rest_framework import serializers
from .models import Cart
from ..products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    product_id = serializers.IntegerField(write_only=True)  # 允许前端仅传 product_id
    product = ProductSerializer(read_only=True)  # 返回完整的 product 数据
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "product", "product_id", "quantity", "added_at", "product_image"]
        extra_kwargs = {"user": {"read_only": True}}  # 确保 user 由系统自动设置

