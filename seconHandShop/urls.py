# seconHandShop/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF 로그인 URL
    path('users/', include('users.urls')),
    path('items/', include('items.urls')),
    path('transactions/', include('transactions.urls')),
    path('chat/', include('chat.urls')),
]
