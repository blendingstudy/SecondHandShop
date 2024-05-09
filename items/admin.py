#items/admin.py

from django.contrib import admin
from .models import Item #, Category

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'price', 'created_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description', 'owner__username']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']