#chat/serializers.py
from django.contrib.messages.storage.cookie import MessageSerializer
from rest_framework import serializers
from .models import Message, ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'title', 'participants', 'messages']
        extra_kwargs = {
            'item': {'write_only': True}
        }

    def get_messages(self, obj):
        messages = obj.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'user', 'user_name', 'text', 'timestamp']
        read_only_fields = ['id', 'user', 'user_name', 'timestamp']
