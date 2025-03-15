"""secondhand_marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


def home_view(request):
    return JsonResponse({"message": "Welcome to Secondhand Marketplace API!"})


urlpatterns = [
    path('', home_view),  # 添加默认首页
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/admin/', include('apps.admin_panel.urls')),  # 添加这一行
]

# 允许 Django 在开发环境下提供媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
