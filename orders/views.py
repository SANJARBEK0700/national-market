from django.shortcuts import render

from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from cart.models import CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("my_orders")

    def form_valid(self, form):

        cart_items = CartItem.objects.filter(user=self.request.user)

        if not cart_items.exists():
            messages.error(self.request, "Savatcha bo'sh")
            return redirect("cart")

        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        order.calculate_total()

        cart_items.delete()

        messages.success(self.request, "Buyurtma muvaffaqiyatli yaratildi!")

        return super().form_valid(form)


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


