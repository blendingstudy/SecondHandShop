# items/urls.py
from django.urls import path
from .views import ItemListView, ItemListAPI, ItemDetailAPI, ItemDetailView, ItemCreateView, ItemUpdateView, \
    CategoryListView, SearchView

app_name = 'items'
urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('api/', ItemListAPI.as_view(), name='item-list'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('create/', ItemCreateView.as_view(), name='item-create'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('search/', SearchView.as_view(), name='search'),

    path('create/', ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('api/<int:pk>/', ItemDetailAPI.as_view(), name='item-detail-api'),
]