from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, AvatarUploadView, AdminOnlyView, ChangePasswordView, \
    UpdateLastLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("upload_avatar/", AvatarUploadView.as_view(), name="upload_avatar"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("admin_only/", AdminOnlyView.as_view(), name="admin_only"),
    path("update_last_login/", UpdateLastLoginView.as_view(), name="update_last_login"),
]
