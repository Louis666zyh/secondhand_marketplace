from django.db import models
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .serializers import TransactionSerializer
from apps.products.models import Product
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from django.contrib.auth.decorators import login_required

class TransactionListView(generics.ListCreateAPIView):
    """List transactions or create a new transaction."""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only see their own transactions."""
        user = self.request.user
        return Transaction.objects.filter(models.Q(buyer=user) | models.Q(seller=user))

    def perform_create(self, serializer):
        product_id = self.request.data.get("product_id")
        if not product_id:
            raise ValidationError({"product_id": "Product ID is required."})
        try:
            product = Product.objects.get(id=product_id)
            if product.status != "available":
                raise ValidationError({"product": "Product is not available."})
            # 设置 seller 为产品的卖家
            serializer.save(buyer=self.request.user, product=product, seller=product.seller)
        except Product.DoesNotExist:
            raise ValidationError({"product": "Product not found."})

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a transaction."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(models.Q(buyer=user) | models.Q(seller=user))

    def perform_update(self, serializer):
        transaction = self.get_object()
        new_status = self.request.data.get("status")
        if new_status:
            if new_status not in ["paid", "shipped", "received", "completed", "cancelled"]:
                raise ValidationError({"status": "Invalid status update."})
            if new_status == "paid" and transaction.status == "pending":
                shipping_address = self.request.data.get("shipping_address")
                payment_method = self.request.data.get("payment_method")
                card_number = self.request.data.get("card_number")
                card_password = self.request.data.get("card_password")
                if payment_method == "credit_card" and not (shipping_address and card_number and card_password):
                    raise ValidationError({"details": "Shipping and payment details are required for credit card payments."})
                transaction.shipping_address = shipping_address
                transaction.payment_method = payment_method
                transaction.payment_date = timezone.now()
            transaction.status = new_status
        serializer.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, buyer=request.user)
        delivery_method = request.data.get('delivery_method')
        shipping_address = request.data.get('shipping_address')
        card_number = request.data.get('card_number')
        card_password = request.data.get('card_password')
        order_serial = request.data.get('order_serial')

        transaction.delivery_method = delivery_method
        if delivery_method == 'shipping':
            if not all([shipping_address, card_number, card_password]):
                return Response({'error': 'All shipping details are required.'}, status=status.HTTP_400_BAD_REQUEST)
            transaction.shipping_address = shipping_address
            transaction.card_number = card_number
            transaction.card_password = card_password
        transaction.order_serial = order_serial
        transaction.status = 'paid'
        transaction.save()
        return Response({'message': 'Order confirmed.'}, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ship_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, seller=request.user)
        if transaction.status != 'paid':
            return Response({'error': 'Order must be paid to ship.'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.status = 'shipped'
        transaction.save()
        return Response({'message': 'Order shipped.'}, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({'error': 'Unauthorized or transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, buyer=request.user)
        if transaction.status != 'shipped' and transaction.delivery_method != 'face-to-face':
            return Response({'error': 'Order must be shipped or a face-to-face transaction to receive.'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.status = 'received'
        transaction.save()
        return Response({'message': 'Order received.'}, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({'error': 'Unauthorized or transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_return(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, buyer=request.user)
        if transaction.status != 'received':
            return Response({'error': 'Order must be received to request a return.'}, status=status.HTTP_400_BAD_REQUEST)
        if transaction.return_status != 'none':
            return Response({'error': 'Return already requested.'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.return_status = 'requested'
        transaction.cancellation_reason = request.data.get('reason', '')
        transaction.save()
        return Response({'message': 'Return requested.'}, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({'error': 'Unauthorized or transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_return(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, seller=request.user)
        if transaction.return_status != 'requested':
            return Response({'error': 'No return request to handle.'}, status=status.HTTP_400_BAD_REQUEST)
        action = request.data.get('action')
        if action not in ['approve', 'deny']:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.return_status = 'approved' if action == 'approve' else 'denied'
        if action == 'approve':
            transaction.status = 'cancelled'
        transaction.save()
        return Response({'message': f'Return {action == "approve" and "approved" or "denied"}.'}, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({'error': 'Unauthorized or transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def order_confirmation(request):
    transaction_id = request.query_params.get('transaction_id')
    order_serial = request.query_params.get('order_serial')
    product_id = request.query_params.get('product_id')
    return render(request, 'transactions/order-confirmation.html', {
        'transaction_id': transaction_id,
        'order_serial': order_serial,
        'product_id': product_id
    })

@login_required
def transaction_detail(request):
    transaction_id = request.GET.get('transaction_id')
    product_id = request.GET.get('product_id')
    if not transaction_id or not product_id:
        return JsonResponse({'error': 'Transaction or product ID missing.'}, status=400)
    try:
        transaction = Transaction.objects.get(id=transaction_id, buyer=request.user)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found.'}, status=404)
    return render(request, 'transactions/transaction.html', {
        'transaction_id': transaction_id,
        'product_id': product_id
    })