# chat/urls.py

from django.urls import path
from .views import ChatRoomListView, ChatRoomDetailView, MessageListView, MessageDetailView, ChatRoomMessageListView

urlpatterns = [
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:chatroom_id>/messages/', ChatRoomMessageListView.as_view(), name='chatroom-message-list'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
