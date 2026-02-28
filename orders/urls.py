from django.urls import path
from .views import *

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("my-orders/", MyOrdersView.as_view(), name="my_orders"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
]