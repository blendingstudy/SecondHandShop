#chat/views.py
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

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
        if item_id is None:
            raise ValidationError({'item': 'This field is required.'})

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise NotFound(detail="No Item matches the given query.", code=404)

        seller = item.owner
        buyer = self.request.user
        chatroom = serializer.save(item=item)
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

class ChatRoomCreateView(LoginRequiredMixin, View):
    def get(self, request):
        item_id = request.GET.get('item')
        item = Item.objects.get(id=item_id)
        seller = item.owner
        buyer = request.user

        # 이미 존재하는 채팅방이 있는지 확인
        chatroom = ChatRoom.objects.filter(item=item, participants=seller).filter(participants=buyer).first()

        if not chatroom:
            # 채팅방이 없으면 새로 생성
            chatroom = ChatRoom.objects.create(item=item)
            chatroom.participants.add(seller, buyer)

        return render(request, 'chat/chatroom_detail.html', {'chatroom': chatroom})

class MessageCreateView(LoginRequiredMixin, View):
    def post(self, request):
        chatroom_id = request.POST.get('chatroom')
        text = request.POST.get('text')

        chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
        user = request.user

        Message.objects.create(chatroom=chatroom, user=user, text=text)

        return redirect('chat:chatroom_detail', pk=chatroom.pk)


class ChatRoomDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        chatroom = get_object_or_404(ChatRoom, pk=pk)
        messages = chatroom.message_set.all().order_by('timestamp')

        if request.GET.get('status'):
            transaction = chatroom.transaction_set.first()
            if transaction:
                item = transaction.item
                transaction.status = request.GET.get('status')
                transaction.save()

                if transaction.status == 'completed':
                    item.is_active = False
                else:
                    item.is_active = True
                item.save()

        return render(request, 'chat/chatroom_detail.html', {'chatroom': chatroom, 'messages': messages})

    def post(self, request, pk):
        chatroom = get_object_or_404(ChatRoom, pk=pk)
        text = request.POST.get('text')

        if text:
            Message.objects.create(chatroom=chatroom, user=request.user, text=text)

        return redirect('chat:chatroom_detail', pk=chatroom.pk)

class ChatRoomListView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = request.user.chatrooms.all()
        return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms})