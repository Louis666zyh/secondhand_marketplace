from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, AvatarUploadView, AdminOnlyView, ChangePasswordView, \
    UpdateLastLoginView, current_user, edit_profile, account_view, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login_api'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("upload_avatar/", AvatarUploadView.as_view(), name="upload_avatar"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("admin_only/", AdminOnlyView.as_view(), name="admin_only"),
    path("update_last_login/", UpdateLastLoginView.as_view(), name="update_last_login"),
    path('current/', current_user, name='current_user'),
    path('edit/', edit_profile, name='edit_profile'),
    path('', account_view, name='account'),
]
