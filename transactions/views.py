# transactions/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Transaction
from items.models import Item
from .serializers import TransactionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        item_id = self.request.data.get('item_id')
        if item_id is None:
            raise ValidationError({'item_id': 'This field is required.'})

        item = get_object_or_404(Item, pk=item_id)
        seller = item.owner

        serializer.save(buyer=self.request.user, seller=seller, item=item)


class TransactionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.seller != request.user:
            return Response({'detail': 'You do not have permission to modify this transaction.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
