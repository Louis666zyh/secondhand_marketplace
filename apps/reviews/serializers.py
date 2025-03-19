# apps/reviews/serializers.py
from rest_framework import serializers
from .models import Review, ReviewImage
from apps.products.serializers import ProductSerializer, UserSerializer
from apps.transactions.models import Transaction

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'review', 'image']
        read_only_fields = ['review']

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()  # 通过 transaction 获取商品
    user = UserSerializer(read_only=True)  # 买家信息
    buyer_username = serializers.CharField(source='user.username', read_only=True)
    buyer_avatar = serializers.CharField(source='user.avatar', read_only=True, allow_null=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'transaction', 'product', 'user', 'buyer_username', 'buyer_avatar', 'rating', 'comment', 'created_at', 'likes', 'images']
        read_only_fields = ['created_at', 'likes', 'user']

    def get_product(self, obj):
        # 从 transaction 中获取商品并序列化
        return ProductSerializer(obj.transaction.product).data

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("评分必须在 1 到 5 之间。")
        return value

    def validate(self, data):
        # 确保 transaction 存在且用户是买家
        transaction_id = self.initial_data.get('transaction')
        if not transaction_id:
            raise serializers.ValidationError({"transaction": "必须提供交易ID。"})
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.buyer != self.context['request'].user:
                raise serializers.ValidationError({"transaction": "您不是该交易的买家，无法评价。"})
            if transaction.status != 'received':
                raise serializers.ValidationError({"transaction": "订单必须已收货才能评价。"})
        except Transaction.DoesNotExist:
            raise serializers.ValidationError({"transaction": "交易不存在。"})
        return data