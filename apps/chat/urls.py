from django.urls import path
from .views import SendMessageView, ChatHistoryView, chat_view, RecentMessagesView

app_name = 'chat'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('<int:user_id>/', ChatHistoryView.as_view(), name='chat-history'),
    path('recent/', RecentMessagesView.as_view(), name='recent-messages'),  # 添加 recent 路由
]