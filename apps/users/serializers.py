from django.templatetags.static import static
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# 🔹 用户注册序列化器
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [ "username", "email", "password" ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data[ "username" ],
            email=validated_data[ "email" ]
        )
        user.set_password(validated_data[ "password" ])  # 确保密码加密
        user.save()
        return user


# 🔹 用户登录序列化器（支持用户名或邮箱）
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data[ "username_or_email" ]
        password = data[ "password" ]

        # 允许用户用用户名或邮箱登录
        user = User.objects.filter(username=username_or_email).first()
        if not user:
            user = User.objects.filter(email=username_or_email).first()

        # 🔹 确保用户存在并且密码正确
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("账户未激活")

            # 🔹 生成 JWT Token
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_superuser": user.is_superuser  # 确保返回管理员信息
                }
            }

        raise serializers.ValidationError("用户名或密码错误")


# 🔹 用户个人信息序列化器
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "id", "username", "email", "is_superuser" ]

        def get_avatar(self, obj):
            if obj.avatar:
                return obj.avatar.url
            return static('img/no-image.png')
