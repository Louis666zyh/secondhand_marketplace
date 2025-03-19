from rest_framework import serializers
from .models import Favorite
from apps.products.serializers import ProductSerializer
from ..products.models import Product


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'added_at']

    def validate(self, data):
        if not data.get('product_id'):
            raise serializers.ValidationError({"product_id": "Product ID is required"})
        return data

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        if Favorite.objects.filter(user=self.context['request'].user, product=product).exists():
            raise serializers.ValidationError({"product": "This product is already in your favorites"})
        return Favorite.objects.create(user=self.context['request'].user, product=product)