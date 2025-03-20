from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'status', 'total_price', 'payment_method', 'created_at', 'approve_payment_button', 'preview_product_image', 'delete_button')
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

    def delete_button(self, obj):
        """Provide a delete button for each transaction"""
        return format_html('<a class="button" href="/admin/transactions/transaction/{}/delete/" style="color:red;">🗑 Delete</a>', obj.id)
    delete_button.short_description = "Delete"

    actions = ['approve_selected_transactions', 'delete_selected_transactions']

    def approve_selected_transactions(self, request, queryset):
        """Bulk approve selected transactions"""
        queryset.update(status="paid")
    approve_selected_transactions.short_description = "Approve selected transactions"

    def delete_selected_transactions(self, request, queryset):
        """Bulk delete selected transactions"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} transaction(s) were deleted successfully.")
    delete_selected_transactions.short_description = "Delete selected transactions"

    def has_delete_permission(self, request, obj=None):
        return True

    def get_urls(self):
        """Add custom URLs for approving and deleting transactions"""
        urls = super().get_urls()
        custom_urls = [
            path('<int:transaction_id>/approve/', self.admin_site.admin_view(self.approve_payment), name='approve-transaction'),
            path('transaction/<int:transaction_id>/delete/', self.admin_site.admin_view(self.delete_transaction), name='delete-transaction'),
        ]
        return custom_urls + urls

    def approve_payment(self, request, transaction_id):
        """Approve payment for a transaction"""
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.status == "pending":
                transaction.status = "paid"
                transaction.save()
                self.message_user(request, f"Payment for transaction #{transaction_id} has been approved.")
            else:
                self.message_user(request, f"Transaction #{transaction_id} cannot be approved because its status is {transaction.status}.", level='error')
        except Transaction.DoesNotExist:
            self.message_user(request, f"Transaction #{transaction_id} does not exist.", level='error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/transactions/transaction/'))

    def delete_transaction(self, request, transaction_id):
        """Delete a transaction"""
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.delete()
            self.message_user(request, f"Transaction #{transaction_id} has been deleted successfully.")
        except Transaction.DoesNotExist:
            self.message_user(request, f"Transaction #{transaction_id} does not exist.", level='error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/transactions/transaction/'))