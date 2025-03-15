from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListView(generics.ListCreateAPIView):
    """List transactions or create a new transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only see their own transactions"""
        return Transaction.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the buyer and ensure product is available"""
        serializer.save(buyer=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only access their own transactions"""
        return Transaction.objects.filter(buyer=self.request.user)

    def perform_update(self, serializer):
        """Ensure only valid status transitions"""
        transaction = self.get_object()
        new_status = self.request.data.get("status")

        if new_status and new_status not in ["paid", "shipped", "completed", "cancelled"]:
            raise ValidationError({"status": "Invalid status update."})

        serializer.save()
