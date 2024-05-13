from rest_framework import generics
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import ItemForm
from django.db.models import Q

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

    def get_queryset(self):
        return Item.objects.filter(is_active=True)

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
    template_name = 'items/item_list.html'

    def get_queryset(self):
        queryset = Item.objects.all()
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', None)
        is_active = self.request.GET.get('is_active', None)

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if category:
            queryset = queryset.filter(category__id=category)

        if is_active:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class SearchResultsView(ListView):
    model = Item
    template_name = 'items/search_results.html'
    context_object_name = 'items'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category_id = self.request.GET.get('category')
        is_active = self.request.GET.get('is_active', None)

        queryset = Item.objects.all()

        if query:
            queryset = queryset.filter(title__icontains=query)

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if is_active:
            queryset = queryset.filter(is_active=True)

        return queryset