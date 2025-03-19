from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListCreateView, product_detail, ProductSellerView, \
    search_view

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/seller/", ProductSellerView.as_view(), name="product-seller"),  # 新增端点
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("detail/<int:pk>/", product_detail, name="product-detail-page"),
    path('search/', search_view, name='search'),
]
