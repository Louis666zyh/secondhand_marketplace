from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListCreateView

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),  # /api/products/
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),  # /api/products/<id>/
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),  # /api/products/categories/
]