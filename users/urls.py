# users/urls.py

from django.urls import path
from .views import UserListView, UserDetailView
from .views import CustomAuthToken

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api-token-auth/', CustomAuthToken.as_view())
]
