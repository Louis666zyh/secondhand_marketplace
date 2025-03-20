from django.urls import path

from .admin import ProductAdmin
from .views import ProductListView, ProductDetailView, CategoryListCreateView, product_detail, ProductSellerView, \
    search_view, ProductDeleteView

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/seller/", ProductSellerView.as_view(), name="product-seller"),  #
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("detail/<int:pk>/", product_detail, name="product-detail-page"),
    path('search/', search_view, name='search'),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
]
