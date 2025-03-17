from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('', include('apps.frontend.urls')),  # 直接映射
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('api/users/', include('apps.users.urls')),
                  path('api/products/', include('apps.products.urls')),
                  path('api/transactions/', include('apps.transactions.urls')),
                  path('api/reviews/', include('apps.reviews.urls')),
                  path('api/chat/', include('apps.chat.urls')),
                  path('api/cart/', include('apps.cart.urls')),
                  path('api/admin/', include('apps.admin_panel.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
