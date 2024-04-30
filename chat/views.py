#chat/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from items.models import Item
from .models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from .serializers import MessageSerializer
from .models import Message


class ChatRoomListView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        item_id = self.request.data.get('item')
        item = get_object_or_404(Item, pk=item_id)
        seller = item.owner
        buyer = self.request.user
        chatroom = serializer.save()
        chatroom.participants.add(seller, buyer)


class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

class ChatRoomMessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs.get('chatroom_id')
        return Message.objects.filter(chatroom__id=chatroom_id)


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chatroom_id = self.request.data.get('chatroom')
        if chatroom_id is None:
            raise ValidationError({'chatroom': 'This field is required.'})

        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            raise NotFound(detail="No ChatRoom matches the given query.", code=404)

        user_name = self.request.user.get_full_name()
        serializer.save(user=self.request.user, chatroom=chatroom, user_name=user_name)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
