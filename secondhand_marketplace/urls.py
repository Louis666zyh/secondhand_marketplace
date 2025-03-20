from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.favorites.views import FavoriteListCreateView
from apps.products.views import product_detail
from apps.transactions.views import transaction_detail
from apps.users import views

urlpatterns = [
                  path('', include('apps.frontend.urls')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/chat/', include('apps.chat.urls', namespace='chat')),
                  path('favorites/', include('apps.favorites.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),  # 包含登录路由
                  path('api/users/', include('apps.users.urls')),
                  path('api/products/', include('apps.products.urls')),
                  path('api/transactions/', include('apps.transactions.urls')),
                  path('api/reviews/', include('apps.reviews.urls')),
                  path('api/cart/', include('apps.cart.urls')),
                  path('detail/<int:pk>/', product_detail, name='product-detail-page'),  # 直接定义在根 URL
                  path('transactions/', transaction_detail, name='transaction-detail'),
                  path('favorites/', include('apps.favorites.urls')),
                  path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
                  path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
                  path('sellsaccount/', views.seller_account_view, name='seller-account'),
                  path('api/users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
                  path('api/follow/<int:seller_id>/', views.follow_seller, name='follow_seller'),
                  path('api/favorites/', FavoriteListCreateView.as_view(), name='favorite-list'),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
