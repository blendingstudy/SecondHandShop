from django.db import models
from django.conf import settings
from django.urls import reverse
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.name

class Item(models.Model):
    # 상품을 게시한 사용자
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    # 상품의 이름
    title = models.CharField(max_length=200)
    # 상품에 대한 상세 설명
    description = models.TextField()
    # 상품 가격
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 상품 카테고리 (ForeignKey를 사용하여 별도의 Category 모델과 연결됩니다.)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    # 상품의 상태 (예: 새 상품, 중고 상품 등)
    condition = models.CharField(max_length=100)
    # 상품 동영상 (하나의 상품에 여러 이미지를 연결하기 위해 별도의 모델을 설정할 수도 있습니다.)
    video = models.FileField(upload_to='item_videos/', null=True, blank=True)
    # 상품 게시 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    # 상품 정보 마지막 수정 날짜
    updated_at = models.DateTimeField(auto_now=True)
    # 상품의 활성/비활성 상태
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