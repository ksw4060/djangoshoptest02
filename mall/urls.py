from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/<int:product_pk>/add/", views.add_to_cart, name="add_to_cart"),
    path("orders/new/", views.order_new, name="order_new"),
    path("orders/<int:pk>/pay/", views.order_pay, name="order_pay"),
    path(
        "orders/<int:order_pk>/check/<int:payment_pk>/",
        views.order_check,
        name="order_check",
    ),
]
