from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
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
        seller = self.request.query_params.get("seller", None)

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

        if not seller and self.request.user.is_authenticated:
            queryset = queryset.exclude(seller=self.request.user)

        print(f"Queryset count: {queryset.count()}")
        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user, is_approved=True)

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
    results = Product.objects.filter(
        name__icontains=query,
        status='available',
        is_approved=True
    ).values('id', 'name', 'price', 'image', 'available_until', 'location')

    results = [
        {
            'id': item['id'],
            'name': item['name'],
            'price': float(item['price']),
            'image': item['image'] if item['image'] else '',
            'available_until': item['available_until'].isoformat() if item['available_until'] else '',
            'location': item['location'] if item['location'] else 'Unknown'
        }
        for item in results
    ]

    return JsonResponse(results, safe=False)

class ProductDeleteView(APIView):
    def delete(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        if request.user.is_staff or request.user == product.seller:
            product.delete()
            return Response({"message": f"Product '{product.name}' has been deleted."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)