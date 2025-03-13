from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只允许商品的拥有者修改商品，其他人只能读取。
    """

    def has_object_permission(self, request, view, obj):
        # 任何人都可以读取
        if request.method in permissions.SAFE_METHODS:
            return True
        # 只有商品的卖家才能修改
        return obj.seller == request.user


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]





