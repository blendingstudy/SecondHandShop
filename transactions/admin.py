# transactions/admin.py
from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'item', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['item__title', 'buyer__username', 'seller__username']
