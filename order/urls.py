from django.urls import path
from .views import (
    CartListCreateView,
    CartItemCreateView,
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("carts/", CartListCreateView.as_view(), name="cart-list-create"),
    path("cart-items/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "orders/<uid>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
]
