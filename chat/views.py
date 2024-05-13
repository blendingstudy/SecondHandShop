from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from items.models import Item
from transactions.models import Transaction
from .models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView

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

        chatroom = ChatRoom.objects.filter(item=item, participants=seller).filter(participants=buyer).first()

        if not chatroom:
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
        return render(request, 'chat/chatroom_detail.html', {'chatroom': chatroom, 'messages': messages})

    def post(self, request, pk):
        chatroom = get_object_or_404(ChatRoom, pk=pk)
        text = request.POST.get('text')

        if not chatroom.transaction:
            self.create_transaction(chatroom)

        if text:
            Message.objects.create(chatroom=chatroom, user=request.user, text=text)

        return redirect('chat:chatroom_detail', pk=chatroom.pk)

    def create_transaction(self, chatroom):
        item = chatroom.item
        seller = item.owner
        buyer = chatroom.participants.exclude(id=seller.id).first()

        if buyer:
            transaction = Transaction.objects.create(item=item, seller=seller, buyer=buyer, status='initiated', chatroom=chatroom)
            chatroom.transaction = transaction
            chatroom.save()

class UpdateTransactionStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        chatroom = get_object_or_404(ChatRoom, pk=pk)
        transaction = chatroom.transaction
        new_status = request.POST.get('status')

        if transaction and transaction.seller == request.user and new_status in [choice[0] for choice in Transaction.STATUS_CHOICES]:
            previous_status = transaction.status
            transaction.status = new_status
            transaction.save()

            if previous_status != 'completed' and new_status == 'completed':
                item = transaction.item
                item.is_active = False
                item.save()

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error'})

class ChatRoomListView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = request.user.chatrooms.all()
        return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms})