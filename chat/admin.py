#chat/admin.py

from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_participants')

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'chatroom', 'timestamp')
    list_filter = ('timestamp', 'chatroom')
    search_fields = ('text', 'user__username', 'chatroom__title')
