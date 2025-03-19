from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Favorite
from .serializers import FavoriteSerializer
from apps.products.models import Product

class FavoriteListCreateView(generics.ListCreateAPIView):
    """List and add items to the user's favorites"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure a user can only add a product once"""
        product_id = self.request.data.get("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"product": "Product not found"})

        if Favorite.objects.filter(user=self.request.user, product=product).exists():
            raise ValidationError({"product": "This product is already in your favorites"})

        serializer.save(user=self.request.user, product=product)

class FavoriteDeleteView(APIView):
    """Remove an item from favorites"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            favorite_item = Favorite.objects.get(id=pk, user=request.user)
            favorite_item.delete()
            return Response({"message": "Item removed from favorites"}, status=204)
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite item not found"}, status=404)