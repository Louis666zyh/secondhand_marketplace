from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path("", ReviewListCreateView.as_view(), name="review-list"),  # ✅ 改成 ReviewListCreateView
    path("<int:pk>/", ReviewDetailView.as_view(), name="review-delete"),
]
