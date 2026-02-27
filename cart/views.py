from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from products.models import Product
from .models import Cart, CartItem


# -----------------------------
# CART DETAIL VIEW
# -----------------------------
class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        items = cart.items.select_related('product').all()

        context['cart'] = cart
        context['items'] = items
        context['total_price'] = cart.total_price
        return context


# -----------------------------
# ADD TO CART
# -----------------------------
class AddToCartView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.stock == 0:
            return redirect('product_detail', slug=product.slug)

        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            if item.quantity < product.stock:
                item.quantity += 1
                item.save()
        else:
            item.quantity = min(1, product.stock)
            item.save()

        return redirect('cart_detail')


# -----------------------------
# REMOVE FROM CART
# -----------------------------
class RemoveFromCartView(LoginRequiredMixin, View):

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return redirect('cart_detail')


# -----------------------------
# UPDATE QUANTITY
# -----------------------------
class UpdateCartItemView(LoginRequiredMixin, View):

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        qty = int(request.POST.get('quantity', 1))
        qty = max(qty, 1)
        qty = min(qty, item.product.stock)

        item.quantity = qty
        item.save()

        return redirect('cart_detail')


# -----------------------------
# AJAX UPDATE
# -----------------------------
class AjaxUpdateCartItemView(LoginRequiredMixin, View):

    def post(self, request, item_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart = get_object_or_404(Cart, user=request.user)
            item = get_object_or_404(CartItem, id=item_id, cart=cart)

            qty = int(request.POST.get('quantity', item.quantity))
            qty = max(1, min(qty, item.product.stock))

            item.quantity = qty
            item.save()

            data = {
                'item_id': item.id,
                'quantity': item.quantity,
                'item_total': item.get_cost(),
                'cart_total': cart.total_price,
            }

            return JsonResponse(data)

        return redirect('cart_detail')