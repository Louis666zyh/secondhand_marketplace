from django.contrib import admin
from django.utils.html import format_html
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'comment', 'created_at', 'delete_button')
    list_filter = ('rating',)
    search_fields = ('user__username', 'product__name', 'comment')
    actions = ['delete_selected_reviews']

    def delete_button(self, obj):
        """Provide a delete button"""
        return format_html('<a class="button" href="/admin/reviews/{}/delete/">🗑️ Delete</a>', obj.id)
    delete_button.short_description = "Delete"

    def delete_selected_reviews(self, request, queryset):
        """Bulk delete selected reviews"""
        queryset.delete()
    delete_selected_reviews.short_description = "Delete selected reviews"
