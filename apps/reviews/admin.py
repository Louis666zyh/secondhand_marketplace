# apps/reviews/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Review, ReviewImage

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_name', 'user', 'rating', 'comment', 'created_at', 'delete_button')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    actions = ['delete_selected_reviews']

    def get_product_name(self, obj):
        try:
            return obj.product.name
        except AttributeError:
            return "Unknown Product"
    get_product_name.short_description = "Product"

    def delete_button(self, obj):
        url = reverse('admin:reviews_review_delete', args=[obj.id])
        return format_html('<a class="button" href="{}">🗑️ Delete</a>', url)
    delete_button.short_description = "Delete"

    def delete_selected_reviews(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} reviews.")
    delete_selected_reviews.short_description = "Delete selected reviews"

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'image', 'image_preview']
    search_fields = ['review__id', 'review__user__username']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"