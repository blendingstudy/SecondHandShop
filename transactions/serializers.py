# transactions/serializers.py

from rest_framework import serializers

from chat.models import ChatRoom
from items.models import Item
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    status = serializers.ChoiceField(choices=Transaction.STATUS_CHOICES)
    chatroom = serializers.SlugRelatedField(queryset=ChatRoom.objects.all(), slug_field='id')

    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'seller', 'item', 'status', 'chatroom', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'seller', 'created_at', 'updated_at']