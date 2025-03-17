from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'price', 'status', 'category', 'seller', 'created_at', 'available_until', 'is_approved', 'preview_image',
    'delete_button')
    list_filter = ('status', 'category', 'is_approved', 'available_until')
    search_fields = ('name', 'description')
    actions = [ 'delete_selected_products' ]
    list_editable = ('price', 'status', 'available_until', 'is_approved', 'category')
    fieldsets = (
        (None, {'fields': (
        'name', 'description', 'price', 'category', 'status', 'available_until', 'is_approved', 'image', 'seller')}),
    )

    def preview_image(self, obj):
        """Display product image in Django Admin"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
        return "No Image"

    preview_image.short_description = "Image"

    def approve_button(self, obj):
        """Provide an approve button"""
        if not obj.is_approved:
            return format_html('<a class="button" href="/admin/products/{}/approve/">✅ Approve</a>', obj.id)
        return "✅ Approved"

    approve_button.short_description = "Approve"

    actions = [ 'approve_selected' ]

    def approve_selected(self, request, queryset):
        """Bulk approve selected products"""
        queryset.update(is_approved=True)

    approve_selected.short_description = "Approve selected products"


    def delete_button(self, obj):
        """Provide a delete button"""
        return format_html('<a class="button" href="/admin/products/{}/delete/">🗑️ Delete</a>', obj.id)
    delete_button.short_description = "Delete"


    def delete_selected_products(self, request, queryset):
        """Bulk delete selected products"""
        queryset.delete()
    delete_selected_products.short_description = "Delete selected products"
