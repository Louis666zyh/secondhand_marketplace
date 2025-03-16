from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Chat Messages"""
    sender = serializers.ReadOnlyField(source="sender.username")  # Read-only sender username
    receiver = serializers.ReadOnlyField(source="receiver.username")  # Read-only receiver username
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "created_at", "product_image"]
        extra_kwargs = {"sender": {"read_only": True}}  # Ensure sender is auto-filled
