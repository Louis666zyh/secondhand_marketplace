from rest_framework import serializers
from apps.chat.models import Message  # 修正导入

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True, required=False)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "sender_username", "receiver_username", "content", "created_at", "product_image"]
        extra_kwargs = {"sender": {"read_only": True}, "receiver": {"read_only": True}}