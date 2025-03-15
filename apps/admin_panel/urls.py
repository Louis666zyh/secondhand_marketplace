from django.urls import path
from .views import ApproveUserView, ApproveProductView, UpdateTransactionStatusView

urlpatterns = [
    path("users/<int:user_id>/", ApproveUserView.as_view(), name="admin-user-approve"),
    path("products/<int:product_id>/approve/", ApproveProductView.as_view(), name="admin-product-approval"),
    path("transactions/<int:transaction_id>/", UpdateTransactionStatusView.as_view(), name="admin-transaction-update"),
]
