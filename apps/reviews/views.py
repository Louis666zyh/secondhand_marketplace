from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    """List all reviews or create a new review."""
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Ensure a user can only post one review per product."""
        product = serializer.validated_data.get("product")
        user = self.request.user

        # 检查用户是否已经对该产品提交过评论
        if Review.objects.filter(product=product, user=user).exists():
            raise ValidationError({"detail": "You have already reviewed this product."})

        serializer.save(user=user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """Ensure only the review owner can update the review."""
        if self.request.user != serializer.instance.user:
            raise ValidationError({"detail": "You do not have permission to edit this review."})
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the review owner can delete the review."""
        if self.request.user != instance.user:
            raise ValidationError({"detail": "You do not have permission to delete this review."})
        instance.delete()
