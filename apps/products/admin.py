from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'status', 'category', 'seller', 'created_at', 'available_until', 'is_approved',
        'preview_image', 'delete_button', 'location'
    )
    list_filter = ('status', 'category', 'is_approved', 'available_until')
    search_fields = ('name', 'description')
    actions = ['delete_selected_products', 'approve_selected']
    list_editable = ('price', 'status', 'available_until', 'is_approved', 'category', 'location')
    fieldsets = (
        (None, {
            'fields': (
                'name', 'description', 'price', 'category', 'status', 'available_until', 'is_approved',
                'seller', 'location', 'image', 'image_preview'
            )
        }),
    )
    readonly_fields = ('image_preview',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"

    preview_image.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" />', obj.image.url)
        return "No Image Uploaded"

    image_preview.short_description = "Current Image"

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)

    approve_selected.short_description = "Approve selected products"

    def delete_button(self, obj):
        delete_url = reverse('product-delete', args=[obj.id])
        return format_html(
            '''
            <a class="button" href="#" onclick="deleteProduct('{}', '{}'); return false;">🗑️ Delete</a>
            <script>
                function deleteProduct(url, productName) {{
                    if (confirm('Are you sure you want to delete the product "' + productName + '"?')) {{
                        fetch(url, {{
                            method: 'DELETE',
                            headers: {{
                                'X-CSRFToken': '{}',
                                'Content-Type': 'application/json',
                            }},
                        }})
                        .then(response => {{
                            if (response.ok) {{
                                alert('Product "' + productName + '" has been deleted.');
                                window.location.reload();
                            }} else {{
                                return response.json().then(data => {{
                                    alert('Error: ' + (data.error || 'Failed to delete product.'));
                                }});
                            }}
                        }})
                        .catch(error => {{
                            alert('Error: ' + error);
                        }});
                    }}
                }}
            </script>
            ''',
            delete_url,
            obj.name,
            self.get_csrf_token()
        )

    delete_button.short_description = "Delete"

    def delete_selected_products(self, request, queryset):
        queryset.delete()

    delete_selected_products.short_description = "Delete selected products"

    def save_model(self, request, obj, form, change):
        # Django 的 ImageField 自动处理图片覆盖逻辑
        super().save_model(request, obj, form, change)

    def get_csrf_token(self):
        from django.middleware.csrf import get_token
        return get_token(self.request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.request = request
        extra_context = extra_context or {}
        # 传递图片上传说明
        extra_context['image_upload_instructions'] = (
            "To add or update the product image, use the 'Image' field below. "
            "If the product already has an image, uploading a new one will replace it. "
            "To remove the existing image, check 'Clear' in the 'Image' field."
        )
        # 获取表单并设置 enctype
        form = self.get_form(request)(instance=self.get_object(request, object_id))
        form.enctype = "multipart/form-data"
        extra_context['form'] = form
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.request = request
        extra_context = extra_context or {}
        # 获取表单并设置 enctype
        form = self.get_form(request)()
        form.enctype = "multipart/form-data"
        extra_context['form'] = form
        return super().add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)