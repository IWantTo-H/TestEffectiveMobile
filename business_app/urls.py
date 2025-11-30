from django.urls import path
from .views import ProductListView, OrderListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('orders/', OrderListView.as_view(), name='orders'),
]