# items/views.py
from rest_framework import generics
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import ItemForm

class ItemListAPI(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ItemDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = '/items/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SearchView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        category = self.request.query_params.get('category', None)

        queryset = Item.objects.filter(is_active=True)

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset