# transactions/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import ValidationError

from chat.models import ChatRoom
from .models import Transaction
from items.models import Item
from .serializers import TransactionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# transactions/views.py

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        status = serializer.validated_data['status']
        chatroom = serializer.validated_data['chatroom']

        participants = chatroom.participants.exclude(id=self.request.user.id)
        if participants.exists():
            buyer = participants.first()
        else:
            raise ValidationError("채팅방에 다른 참여자가 없습니다.")

        seller = item.owner

        serializer.save(buyer=buyer, seller=seller, item=item, status=status)

        seller = item.owner

        serializer.save(buyer=buyer, seller=seller, item=item, status=status, chatroom=chatroom)



class TransactionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.seller != request.user:
            return Response({'detail': 'You do not have permission to modify this transaction.'},
                            status=status.HTTP_403_FORBIDDEN)

        previous_status = transaction.status
        serializer = self.get_serializer(transaction, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        transaction.refresh_from_db()

        if previous_status != 'completed' and transaction.status == 'completed':
            item = transaction.item
            item.is_active = False
            item.save()

        return Response(serializer.data)

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(buyer=user) | Q(seller=user))
