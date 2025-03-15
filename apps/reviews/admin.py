from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username", "rating")
    list_filter = ("rating", "created_at")
