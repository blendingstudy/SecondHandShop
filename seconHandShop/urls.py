# secondHandShop/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF 로그인 URL
    path('users/', include('users.urls')),
    path('items/', include('items.urls')), # 이 부분만 남겨둡니다.
    path('transactions/', include('transactions.urls')),
    path('chat/', include('chat.urls')),
    path('', UserLoginView.as_view(), name='login'),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
    path('transactions/', include('transactions.urls', namespace='transactions')),  #
]
