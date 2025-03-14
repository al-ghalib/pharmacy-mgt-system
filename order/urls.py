from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<uuid:uid>', views.CartDetailView.as_view(), name='cart-detail'),

    path('cart-items', views.CartItemListCreateView.as_view(), name='cart-item-list-create'),

    path('order', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('order/<uuid:uid>', views.OrderDetailView.as_view(), name='order-detail'),

    path('order-details', views.OrderDetailsListView.as_view(), name='order-details-list'),
]
