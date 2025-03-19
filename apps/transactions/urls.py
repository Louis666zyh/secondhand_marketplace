from django.urls import path
from .views import (TransactionListView, TransactionDetailView, confirm_transaction, order_confirmation,
                    ship_transaction, receive_transaction, request_return, handle_return)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction-list"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path('<int:transaction_id>/confirm/', confirm_transaction, name='confirm-transaction'),
    path('<int:transaction_id>/ship/', ship_transaction, name='ship-transaction'),
    path('<int:transaction_id>/receive/', receive_transaction, name='receive-transaction'),
    path('<int:transaction_id>/return/request/', request_return, name='request-return'),
    path('<int:transaction_id>/return/handle/', handle_return, name='handle-return'),
    path('order-confirmation/', order_confirmation, name='order-confirmation'),
]