from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions: Only the owner of the product is allowed to modify the product, while others can only read it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user


class ProductListView(generics.ListCreateAPIView):
    """ Product List & Create Product"""
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly ]
    parser_classes = [ MultiPartParser, FormParser ]
    filter_backends = [ DjangoFilterBackend, SearchFilter, OrderingFilter ]
    filterset_fields = [ "status" ]
    search_fields = [ "name", "description" ]
    ordering_fields = [ "price", "created_at" ]

    def get_queryset(self):
        """ 按类别筛选商品 """
        queryset = Product.objects.all().order_by("-created_at")
        category = self.request.query_params.get("category", None)
        search = self.request.query_params.get("search", None)
        available_until = self.request.query_params.get("available_until__lte", None)

        if category:
            # 查找匹配的类别名称
            try:
                queryset = queryset.filter(category__name__iexact=category, is_approved=True)
            except Category.DoesNotExist:
                queryset = Product.objects.none()  # 如果类别不存在，返回空结果
        else:
            queryset = queryset.filter(is_approved=True)

        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        if available_until:
            try:
                # 直接使用 YYYY-MM-DD 格式，因为前端传递的是日期字符串
                queryset = queryset.filter(available_until__lte=available_until)
            except ValueError as e:
                print(f"Invalid date format for available_until: {available_until}, error: {e}")
                queryset = queryset.none()

        print(f"Queryset count: {queryset.count()}")

        return queryset


def perform_create(self, serializer):
    serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Product Details & Update & Delete"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ IsOwnerOrReadOnly ]

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.seller:
            serializer.save()


class CategoryListCreateView(generics.ListCreateAPIView):
    """ Category List & Create Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly ]


from django.http import JsonResponse
from .models import Product


def product_list(request):
    category = request.GET.get('category', None)

    # 按类别筛选商品
    if category:
        products = Product.objects.filter(category__name=category, is_approved=True)
    else:
        products = Product.objects.filter(is_approved=True)

    # 返回 JSON 数据
    data = [ {"id": p.id, "name": p.name, "price": p.price, "image": p.image.url if p.image else "",
              "location": p.seller.profile.location} for p in products ]
    return JsonResponse(data, safe=False)
