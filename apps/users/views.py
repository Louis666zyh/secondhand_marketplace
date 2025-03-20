from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Profile, Follow
from ..transactions.models import Transaction

User = get_user_model()

class UserProfileView(APIView):
    """Handles user profile retrieval, modification, and deletion"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve user profile"""
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None
        })

    def patch(self, request):
        """Modify username & email"""
        user = request.user
        username = request.data.get("username")
        email = request.data.get("email")

        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            user.username = username

        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            user.email = email

        user.save()
        return Response({"message": "Profile updated successfully", "username": user.username, "email": user.email})

    def delete(self, request):
        """Delete user account"""
        user = request.user
        user.delete()
        return Response({"message": "Account deleted"}, status=status.HTTP_204_NO_CONTENT)


class AvatarUploadView(APIView):
    """Handles user avatar upload"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        file = request.FILES.get("avatar")
        if not file:
            return Response({"error": "请上传头像文件"}, status=status.HTTP_400_BAD_REQUEST)
        if user.avatar:
            default_storage.delete(user.avatar.path)
        user.avatar = file
        user.save()
        return Response({"avatar": request.build_absolute_uri(user.avatar.url)}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """User registration API"""
    permission_classes = [ AllowAny ]
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not all([username, email, password, first_name, last_name]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")

        if not username_or_email or not password:
            return Response({"error": "username_or_email and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username_or_email).first()
        if not user:
            user = User.objects.filter(email=username_or_email).first()

        if user and user.check_password(password):
            if not user.is_active:
                return Response({"error": "Account is inactive"}, status=status.HTTP_400_BAD_REQUEST)

            login(request, user)  # 设置 Django 会话
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_superuser": user.is_superuser
                },
                "redirect": request.GET.get('next', '/account/')  # 返回重定向 URL
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateLastLoginView(APIView):
    """Manually update last_login when user is active"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_login = now()
        user.save(update_fields=["last_login"])
        return Response({"message": "Last login updated", "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S")})


class AdminOnlyView(APIView):
    """API accessible only to admin users"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome, Admin!"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """API to change user password"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 清除 Django 会话
            logout(request)
            # 清除 localStorage 中的令牌（前端负责）
            return HttpResponseRedirect(reverse('login') + '?next=/sell-item/')  # 重定向到登录页面
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None
    }
    return Response(data)

@login_required
def profile_view(request):
    return render(request, 'profile.html', {})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.save()
        profile = user.profile
        profile.bio = request.POST.get('bio', profile.bio)
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()
        profile.save()
        return redirect('account')  # 重定向到账户页面
    # 如果是GET请求，返回编辑页面
    return render(request, 'edit_profile.html', {'user': request.user})


# apps/users/views.py
from django.shortcuts import render
from .models import Profile

def account_view(request):
    # 确保用户有 Profile 实例
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    # 处理 listings 数据
    listings_data = [
        {
            "id": product.id,
            "title": str(product.name) if product.name else "",
            "price": float(product.price) if product.price else 0.0,
            "image": product.image.url if product.image and hasattr(product.image, 'url') else ""
        }
        for product in request.user.products.all()  # 改为 user.products
    ]

    # 处理 likes 数据
    likes_data = [
        {
            "id": favorite.product.id,
            "title": str(favorite.product.name) if favorite.product.name else "",
            "price": float(favorite.product.price) if favorite.product.price else 0.0,
            "image": favorite.product.image.url if favorite.product.image and hasattr(favorite.product.image, 'url') else ""
        }
        for favorite in request.user.favorites.all()
    ]

    # 处理 reviews 数据
    reviews_data = [
        {
            "user": str(review.user.username) if review.user.username else "",
            "rating": float(review.rating) if review.rating else 0.0,
            "comment": str(review.comment) if review.comment else ""
        }
        for review in request.user.reviews.all()
    ]

    # 确保所有数据都是 JSON 兼容格式
    context = {
        "listings_data": listings_data if listings_data else [],
        "likes_data": likes_data if likes_data else [],
        "reviews_data": reviews_data if reviews_data else [],
        "user_profile": {
            "id": request.user.profile.id if hasattr(request.user, 'profile') else None,
            "bio": request.user.profile.bio if hasattr(request.user, 'profile') else "",
            "avatar": request.user.avatar.url if hasattr(request.user, 'profile') and request.user.avatar else ""
        }
    }
    return render(request, 'account.html', context)

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            # 计算完成的交易数量
            transactions = Transaction.objects.filter(product__seller=user, status='completed').count()
            # 计算总交易数量（不包括 pending 状态）
            total_transactions = Transaction.objects.filter(product__seller=user).exclude(status='pending').count()
            # 计算取消的交易数量（作为退货的近似）
            cancelled_transactions = Transaction.objects.filter(product__seller=user, status='cancelled').count()
            # 计算退货率
            return_rate = (cancelled_transactions / total_transactions * 100) if total_transactions > 0 else 0
            # 计算关注者数量
            followers = user.followers.count()

            data = {
                "id": user.id,
                "username": user.username,
                "avatar": user.avatar.url if user.avatar else None,
                "location": user.location,
                "transactions": transactions,
                "followers": followers,
                "return_rate": round(return_rate, 2)
            }
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@login_required
def seller_account_view(request):
    seller_id = request.GET.get('seller_id')
    if not seller_id:
        return redirect('home')  # 如果没有 seller_id，重定向到首页

    # 渲染 sellsaccount.html，传递 seller_id
    return render(request, 'sellsaccount.html', {'seller_id': seller_id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        followers_count = Follow.objects.filter(followee=user).count()
        data = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar.url if user.avatar else "https://placekitten.com/120/120",
            'location': user.location or "Unknown",
            'transactions': user.profile.transactions if hasattr(user, 'profile') else 0,
            'followers': followers_count,
            'return_rate': user.profile.return_rate if hasattr(user, 'profile') else 0,
        }
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def follow_seller(request, seller_id):
    try:
        seller = User.objects.get(id=seller_id)
    except User.DoesNotExist:
        return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 检查是否已关注
        followed = Follow.objects.filter(follower=request.user, followee=seller).exists()
        return Response({'followed': followed}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 关注或取消关注
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=seller)
        if not created:
            # 如果已经关注，则取消关注
            follow.delete()
            return Response({'followed': False}, status=status.HTTP_200_OK)
        return Response({'followed': True}, status=status.HTTP_201_CREATED)