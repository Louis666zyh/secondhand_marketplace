from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect
from .models import User

class CustomUserAdmin(UserAdmin):
    """Customize the User model for Django Admin"""

    list_display = ("id", "username", "email", "is_staff", "is_superuser", "delete_button")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    # 添加删除按钮
    def delete_button(self, obj):
        """Provide a delete button for each user"""
        return format_html('<a class="button" href="/admin/users/user/{}/delete/" style="color:red;">🗑 Delete</a>', obj.id)
    delete_button.short_description = "Delete"


    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        """Bulk delete selected users"""
        count = queryset.count()
        for user in queryset:
            user.delete()
        self.message_user(request, f"{count} user(s) were deleted successfully.")
    delete_selected_users.short_description = "Delete selected users"

    def has_delete_permission(self, request, obj=None):
        return True

    def get_urls(self):
        """Add custom URLs for deleting users"""
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/delete/', self.admin_site.admin_view(self.delete_user), name='delete-user'),
        ]
        return custom_urls + urls

    def delete_user(self, request, user_id):
        """Delete a user"""
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            self.message_user(request, f"User '{user.username}' (ID: {user_id}) has been deleted successfully.")
        except User.DoesNotExist:
            self.message_user(request, f"User with ID {user_id} does not exist.", level='error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/users/user/'))

admin.site.register(User, CustomUserAdmin)
