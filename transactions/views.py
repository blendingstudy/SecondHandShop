from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from chat.models import ChatRoom
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView
from .models import Transaction

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(buyer=user) | Q(seller=user))

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        chatroom = serializer.validated_data['chatroom']
        seller = item.owner
        buyer = chatroom.participants.exclude(id=seller.id).first()

        if buyer:
            serializer.save(buyer=buyer, seller=seller, item=item, status='initiated', chatroom=chatroom)
        else:
            raise ValidationError("채팅방에 다른 참여자가 없습니다.")

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

        if previous_status != 'completed' and transaction.status == 'completed':
            item = transaction.item
            item.is_active = False
            item.save()

        return Response(serializer.data)

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(buyer=user) | Q(seller=user), status='completed')