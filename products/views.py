from django.shortcuts import render

from django.shortcuts import render
from .models import Product, Category


def index_view(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context)


from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import Product


from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Product

def my_products_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    my_products = Product.objects.filter(seller=request.user).select_related('category').order_by('-created_at')

    query = request.GET.get('q', '').strip()
    if query:
        my_products = my_products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'my_products': my_products,
        'search_query': query,
    }

    return render(request, 'my_products.html', context)




def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category

from decimal import Decimal


def product_edit_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, pk=pk, seller=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        try:
            price = Decimal(request.POST.get('price', '0'))

            discount_raw = request.POST.get('discount_price')
            if discount_raw and discount_raw.strip():
                discount_price = Decimal(discount_raw)
            else:
                discount_price = None
        except (ValueError, TypeError, ):
            messages.error(request, "Narx noto'g'ri kiritildi.")
            return render(request, 'product_form.html', {'product': product, 'categories': categories})

        # Modelni yangilash
        product.title = title
        product.price = price  # Endi bu Decimal tipida
        product.discount_price = discount_price
        product.description = description

        if category_id:
            product.category = get_object_or_404(Category, id=category_id)

        main_image = request.FILES.get('main_image')
        if main_image:
            product.main_image = main_image

        # Save chaqirilganda models.py dagi matematik amallar xatosiz ishlaydi
        product.save()

        messages.success(request, "Mahsulot muvaffaqiyatli yangilandi!")
        return redirect('my_products')

    return render(request, 'product_form.html', {'product': product, 'categories': categories})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        product.delete()
        messages.warning(request, "Mahsulot o'chirildi.")
        return redirect('my_products')

    return redirect('my_products')
