#items/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    condition = models.CharField(max_length=100)
    video = models.FileField(upload_to='item_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:item-detail', kwargs={'pk': self.pk})

# @receiver(post_migrate)
# def create_initial_categories(sender, **kwargs):
#     if sender.name == 'items':
#         Category = sender.get_model('Category')
#         if not Category.objects.exists():
#             category_list = [
#                 '전자기기',
#                 '가구',
#                 '의류',
#                 '스포츠용품',
#                 '책',
#             ]
#
#             for cat_name in category_list:
#                 Category.objects.create(name=cat_name)