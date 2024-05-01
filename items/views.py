#items/views.py

from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자만 생성 가능, 읽기는 누구나 가능

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # 상품을 생성할 때 owner를 현재 사용자로 설정

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자만 수정/삭제 가능
