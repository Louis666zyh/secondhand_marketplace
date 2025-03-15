from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SendMessageView(generics.CreateAPIView):
    """Send a chat message"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure sender is set automatically"""
        serializer.save(sender=self.request.user)

class ChatHistoryView(APIView):
    """Retrieve chat history with a specific user"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """Get chat messages between the authenticated user and another user"""
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        messages = Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user]
        ).order_by("created_at")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
