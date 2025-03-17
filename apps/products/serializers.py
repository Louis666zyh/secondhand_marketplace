from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories"""
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products"""
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField(required=False)
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = '__all__'
