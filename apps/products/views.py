from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")
        category = self.request.query_params.get("category", None)
        search = self.request.query_params.get("search", None)
        available_until = self.request.query_params.get("available_until__lte", None)
        location = self.request.query_params.get("location", None)
        seller = self.request.query_params.get("seller", None)  # 新增 seller 参数

        if seller:
            try:
                queryset = queryset.filter(seller_id=seller, is_approved=True, status='available')
            except ValueError:
                queryset = Product.objects.none()
        else:
            queryset = queryset.filter(is_approved=True)

        if category:
            try:
                queryset = queryset.filter(category__name__iexact=category, is_approved=True)
            except Category.DoesNotExist:
                queryset = Product.objects.none()

        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        if available_until:
            try:
                queryset = queryset.filter(available_until__lte=available_until)
            except ValueError as e:
                print(f"Invalid date format for available_until: {available_until}, error: {e}")
                queryset = Product.objects.none()

        if location:
            queryset = queryset.filter(location__iexact=location)

        # 排除当前用户的商品（仅在未指定 seller 参数时应用）
        if not seller and self.request.user.is_authenticated:
            queryset = queryset.exclude(seller=self.request.user)

        print(f"Queryset count: {queryset.count()}")
        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(is_approved=True)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.seller or self.request.user.is_staff:
            serializer.save()

class ProductSellerView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_approved=True)
        seller = product.seller
        seller_data = {
            'id': seller.id,
            'username': seller.username,
            'avatar': seller.avatar.url if hasattr(seller, 'avatar') and seller.avatar else "https://via.placeholder.com/50"
        }
        return Response(seller_data)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_approved=True)
    return render(request, 'detail.html', {'product_id': pk})

def search_view(request):
    query = request.GET.get('q', '')
    # 使用 Product 模型，并确保只搜索可用商品
    results = Product.objects.filter(
        name__icontains=query,
        status='available',  # 仅显示可用商品
        is_approved=True  # 仅显示已批准的商品
    ).values('id', 'name', 'price', 'image', 'available_until', 'location')

    # 处理 image 字段，确保返回 URL
    results = [
        {
            'id': item['id'],
            'name': item['name'],
            'price': float(item['price']),  # Decimal 转换为 float
            'image': item['image'] if item['image'] else '',  # 确保 image 字段不为空
            'available_until': item['available_until'].isoformat() if item['available_until'] else '',
            'location': item['location'] if item['location'] else 'Unknown'
        }
        for item in results
    ]

    return JsonResponse(results, safe=False)