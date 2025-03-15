from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Chat Messages"""
    sender = serializers.ReadOnlyField(source="sender.username")  # Read-only sender username
    receiver = serializers.ReadOnlyField(source="receiver.username")  # Read-only receiver username

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "created_at"]
        extra_kwargs = {"sender": {"read_only": True}}  # Ensure sender is auto-filled
