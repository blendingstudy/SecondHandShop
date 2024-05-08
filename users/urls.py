# users/urls.py

from django.urls import path
from .views import UserListView, UserDetailView, UserLoginView, UserRegisterView, UserProfileView, UserLogoutView
from .views import CustomAuthToken
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api-token-auth/', CustomAuthToken.as_view()),

    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
