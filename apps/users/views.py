from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now

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
        """Upload user avatar"""
        user = request.user
        file = request.FILES.get("avatar")

        if not file:
            return Response({"error": "Please upload an avatar file"}, status=status.HTTP_400_BAD_REQUEST)

        if user.avatar:
            default_storage.delete(user.avatar.path)

        user.avatar = file
        user.save()
        return Response({"avatar": request.build_absolute_uri(user.avatar.url)}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """User registration API"""

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
    """User login API (supports username or email)"""
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")

        user = User.objects.filter(username=username_or_email).first()
        if not user:
            user = User.objects.filter(email=username_or_email).first()

        if user and user.check_password(password):
            if not user.is_active:
                return Response({"error": "Account is inactive"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_superuser": user.is_superuser
                }
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
