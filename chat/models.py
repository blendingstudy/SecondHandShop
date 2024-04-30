#chat/models.py

from django.db import models
from django.conf import settings

from items.models import Item
from users.models import CustomUser


class ChatRoom(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='chatrooms')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    messages = models.ManyToManyField('Message', related_name='chatrooms')

    @property
    def title(self):
        return self.item.title

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
