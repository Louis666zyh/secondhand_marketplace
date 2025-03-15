from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.products.models import Product
from apps.transactions.models import Transaction
from .serializers import AdminUserSerializer, AdminProductSerializer, AdminTransactionSerializer

class ApproveUserView(APIView):
    """API for admin to approve user accounts."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = AdminUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User approval updated", "is_approved": user.is_approved})
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class ApproveProductView(APIView):
    """API for admin to approve products."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = AdminProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product approval updated", "is_approved": product.is_approved})
            return Response(serializer.errors, status=400)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

class UpdateTransactionStatusView(APIView):
    """API for admin to update transaction status."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            serializer = AdminTransactionSerializer(transaction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Transaction status updated", "status": transaction.status})
            return Response(serializer.errors, status=400)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)