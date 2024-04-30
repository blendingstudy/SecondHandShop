from rest_framework import serializers
from .models import Item, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category = serializers.ChoiceField(
        choices=[(category.id, category.name) for category in Category.objects.all()],
        allow_null=True,
        required=False
    )
    video = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'owner', 'title', 'description', 'price', 'category', 'category_name', 'condition', 'video', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['owner', 'category_name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = CategorySerializer(instance.category).data
        return representation

    def get_video(self, obj):
        if obj.video:
            return self.context['request'].build_absolute_uri(obj.video.url)
        return None