from django.urls import path
from .views import SendMessageView, ChatHistoryView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('<int:user_id>/', ChatHistoryView.as_view(), name='chat-history'),
]
