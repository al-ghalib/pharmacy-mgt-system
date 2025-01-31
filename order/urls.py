from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<uuid:pk>/', views.CartDetailView.as_view(), name='cart-detail'),

    path('cart-item/', views.CartItemListCreateView.as_view(), name='cart-item-list-create'),

    path('order/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('order/<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),

    path('order-detail/', views.OrderDetailItemListCreateView.as_view(), name='order-detail-list-create'),
]
