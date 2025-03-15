from django.urls import path
from .views import CartListCreateView, CartUpdateView, CartDeleteView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart-list'),
    path('<int:pk>/', CartUpdateView.as_view(), name='cart-update'),
    path('<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),
]
