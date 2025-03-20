from django.db.models import Max, Q
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from apps.chat.models import Message
from apps.chat.serializers import MessageSerializer
from django.contrib.auth import get_user_model
from apps.products.models import Product
from datetime import datetime

User = get_user_model()

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        content = self.request.data.get('content')
        if not receiver_id or not content:
            raise serializers.ValidationError({"error": "Receiver and content cannot be empty"})
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found"}, status=404)

        # 防止用户给自己发送消息
        if receiver == self.request.user:
            raise serializers.ValidationError({"error": "You cannot send a message to yourself"})

        message = serializer.save(sender=self.request.user, receiver=receiver)
        return Response(MessageSerializer(message).data, status=201)

class ChatHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        last_time = request.query_params.get('since', None)
        messages = Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user]
        ).order_by("-created_at")

        if last_time:
            try:
                # 将毫秒时间戳转换为 datetime 对象
                last_time_ms = int(last_time)  # 确保是整数
                last_time_dt = datetime.fromtimestamp(last_time_ms / 1000.0)  # 转换为秒并生成 datetime
                messages = messages.filter(created_at__gt=last_time_dt)
            except (ValueError, TypeError) as e:
                return Response({"error": "Invalid 'since' parameter format. Use a valid timestamp in milliseconds."},
                                status=400)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    seller_id = request.GET.get('seller')
    product_id = request.GET.get('product')
    selected_product = None
    if product_id:
        try:
            selected_product = get_object_or_404(Product, pk=product_id, is_approved=True)
        except:
            pass
    return render(request, 'chat.html', {'users': users, 'selected_product': selected_product})

class RecentMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取当前用户最近的聊天记录，每个用户只返回最新一条消息"""
        latest_messages = Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).values("sender", "receiver").annotate(last_msg=Max("created_at"))

        messages = Message.objects.filter(
            created_at__in=[msg["last_msg"] for msg in latest_messages]
        ).select_related("sender", "receiver").order_by("-created_at")

        serializer = MessageSerializer(messages, many=True)

        # 过滤掉当前用户自己的消息
        recent_chats = []
        seen_users = set()
        for message in serializer.data:
            other_user_id = message['receiver'] if message['sender'] == request.user.id else message['sender']
            if other_user_id == request.user.id:  # 排除当前用户
                continue
            if other_user_id not in seen_users:
                seen_users.add(other_user_id)
                other_user = User.objects.get(id=other_user_id)
                recent_chats.append({
                    'sender': message['sender'],
                    'receiver': message['receiver'],
                    'sender_username': request.user.username if message['sender'] == request.user.id else other_user.username,
                    'receiver_username': request.user.username if message['receiver'] == request.user.id else other_user.username,
                    'content': message['content'],
                    'created_at': message['created_at'],
                    'sender_avatar': other_user.avatar.url if other_user.avatar else None
                })

        return Response(recent_chats)