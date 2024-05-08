# chat/urls.py

from django.urls import path
from .views import ChatRoomListView, ChatRoomDetailView, MessageListView, MessageDetailView, ChatRoomMessageListView, \
    ChatRoomCreateView, MessageCreateView

app_name = 'chat'

urlpatterns = [
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom_list'),
    path('chatrooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chatroom_detail'),
    path('chatrooms/<int:chatroom_id>/messages/', ChatRoomMessageListView.as_view(), name='chatroom_message_list'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),

    path('chatrooms/create/', ChatRoomCreateView.as_view(), name='chatroom_create'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
]