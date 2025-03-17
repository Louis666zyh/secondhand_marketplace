from django.contrib import admin
from django.utils.html import format_html
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'status', 'total_price', 'payment_method', 'created_at', 'approve_payment_button', 'preview_product_image')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_reference', 'buyer__username')

    def preview_product_image(self, obj):
        """Display the product image related to the transaction"""
        if obj.product.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.product.image.url)
        return "No Image"
    preview_product_image.short_description = "Product Image"

    def approve_payment_button(self, obj):
        """Provide an approve payment button"""
        if obj.status == "pending":
            return format_html('<a class="button" href="/admin/transactions/{}/approve/">💰 Approve Payment</a>', obj.id)
        return "✅ Payment Approved"
    approve_payment_button.short_description = "Approve Payment"

    actions = ['approve_selected_transactions']

    def approve_selected_transactions(self, request, queryset):
        """Bulk approve selected transactions"""
        queryset.update(status="paid")
    approve_selected_transactions.short_description = "Approve selected transactions"

    def has_delete_permission(self, request, obj=None):
        return True


    def delete_button(self, obj):
        return format_html(f'<a href="/admin/transactions/order/{obj.id}/delete/" style="color:red;">🗑 Delete</a>')

    delete_button.allow_tags = True
    delete_button.short_description = 'Delete'
