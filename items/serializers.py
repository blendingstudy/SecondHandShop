#items/serializers.py

from rest_framework import serializers
from .models import Item, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    video = serializers.FileField(required=False)

    class Meta:
        model = Item
        fields = ['id', 'owner', 'title', 'description', 'price', 'condition', 'video', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['owner']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = CategorySerializer(instance.category).data
        return representation

    def get_video(self, obj):
        if obj.video:
            return self.context['request'].build_absolute_uri(obj.video.url)
        return None

    def perform_create(self, serializer):
        video = self.request.FILES.get('video', None)
        serializer.save(owner=self.request.user, video=video)