# transactions/urls.py

from django.urls import path
from .views import TransactionListCreateView, TransactionDetailView, TransactionListView

app_name = 'transactions'
urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
