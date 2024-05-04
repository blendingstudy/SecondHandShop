# transactions/models.py

from django.db import models
from django.conf import settings

from chat.models import ChatRoom


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions_as_buyer', on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions_as_seller', on_delete=models.CASCADE)
    item = models.ForeignKey('items.Item', related_name='transactions', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction for {self.item.title} by {self.buyer.username}"
