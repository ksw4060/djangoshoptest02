from django.urls import path
from mall_test import views

# app_name = "mall_test"
urlpatterns = [
    path("payment/new/", views.payment_new, name="payment_new"),
    path("payment/<int:pk>/pay/", views.payment_pay, name="payment_pay"),
    path("payment/<int:pk>/check/", views.payment_check, name="payment_check"),
    path("payment/<int:pk>/", views.payment_detail, name="payment_detail"),
]
