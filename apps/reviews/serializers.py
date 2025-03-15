from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews"""
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "comment", "created_at"]
        extra_kwargs = {"user": {"read_only": True}}
