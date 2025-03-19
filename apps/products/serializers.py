from rest_framework import serializers
from .models import Product, Category
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories"""

    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products"""
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField(required=False)
    category = serializers.CharField(source='category.name', required=True)  # 用于读取和写入 category 名称

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'is_approved']

    def to_internal_value(self, data):
        # 处理 category 字段：将传入的 category 名称转换为 Category 实例
        internal_data = super().to_internal_value(data)
        category_name = internal_data.get('category', {}).get('name') if 'category' in internal_data else None
        if category_name:
            try:
                category_instance = Category.objects.get(name=category_name)
                internal_data['category'] = category_instance
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": f"Category '{category_name}' does not exist."})
        return internal_data

    def create(self, validated_data):
        # 提取字段
        category_instance = validated_data.pop('category', None)  # 已经由 to_internal_value 转换为 Category 实例
        image = validated_data.pop('image', None)
        available_until = validated_data.pop('available_until', None)
        location = validated_data.pop('location', None)

        # seller 已由 perform_create 注入到 validated_data 中，无需显式传递
        product = Product.objects.create(
            category=category_instance,
            image=image,
            available_until=available_until,
            location=location,
            **validated_data
        )
        return product

    def update(self, instance, validated_data):
        # 提取字段
        category_instance = validated_data.pop('category', None)
        image = validated_data.pop('image', None)
        available_until = validated_data.pop('available_until', None)
        location = validated_data.pop('location', None)

        # 更新实例
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.status = validated_data.get('status', instance.status)
        instance.location = validated_data.get('location', instance.location)
        instance.category = category_instance if category_instance else instance.category
        instance.image = image if image else instance.image
        instance.available_until = available_until if available_until else instance.available_until
        instance.location = location if location else instance.location
        instance.save()
        return instance