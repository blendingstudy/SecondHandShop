# transactions/serializers.py

from rest_framework import serializers

from chat.models import ChatRoom
from items.models import Item
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    chatroom_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=ChatRoom.objects.all(),
        source='chatroom'
    )

    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'seller', 'item', 'status', 'created_at', 'updated_at', 'chatroom_id']
        read_only_fields = ['id', 'buyer', 'seller', 'created_at', 'updated_at']
        extra_kwargs = {
            'chatroom': {'read_only': True}
        }
