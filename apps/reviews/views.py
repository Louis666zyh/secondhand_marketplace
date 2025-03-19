# apps/reviews/views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer
from apps.transactions.models import Transaction
from rest_framework.pagination import LimitOffsetPagination

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Review.objects.all().order_by("-created_at")
        seller = self.request.query_params.get("seller", None)

        if seller:
            try:
                # Filter out all reviews related to the seller's transactions
                queryset = queryset.filter(transaction__seller_id=seller)
            except ValueError:
                queryset = Review.objects.none()

        return queryset

    def perform_create(self, serializer):
        transaction_id = self.request.data.get("transaction")
        user = self.request.user

        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            raise ValidationError({"detail": "Transaction does not exist."})

        if transaction.buyer != user:
            raise ValidationError({"detail": "You are not the buyer of this transaction and cannot leave a review."})

        if Review.objects.filter(transaction=transaction, user=user).exists():
            raise ValidationError({"detail": "You have already reviewed this transaction."})

        serializer.save(user=user, transaction=transaction)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise ValidationError({"detail": "You do not have permission to edit this review."})
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise ValidationError({"detail": "You do not have permission to delete this review."})
        instance.delete()