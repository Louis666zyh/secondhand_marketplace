from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart
from .serializers import CartSerializer
from apps.products.models import Product
from ..products import serializers


class CartListCreateView(generics.ListCreateAPIView):
    """List and add items to the shopping cart"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure a user can only add a product once, update quantity if exists"""
        product_id = self.request.data.get("product_id")
        quantity = self.request.data.get("quantity", 1)

        # 确保 product 存在
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product": "Product not found"})

        # 获取用户购物车条目
        cart_item, created = Cart.objects.get_or_create(user=self.request.user, product=product)

        # 如果已存在该商品，则更新数量
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save(update_fields=["quantity"])
        else:
            serializer.save(user=self.request.user, product=product, quantity=quantity)

class CartUpdateView(APIView):
    """Update quantity of a cart item"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            cart_item = Cart.objects.get(id=pk, user=request.user)
            new_quantity = request.data.get("quantity", cart_item.quantity)
            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity"])
            return Response({"message": "Cart updated", "quantity": cart_item.quantity})
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

class CartDeleteView(APIView):
    """Delete a cart item"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item = Cart.objects.get(id=pk, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=204)
        except Cart.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
