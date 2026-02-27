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

        product.title = title
        product.price = price
        product.discount_price = discount_price
        product.description = description

        if category_id:
            product.category = get_object_or_404(Category, id=category_id)

        main_image = request.FILES.get('main_image')
        if main_image:
            product.main_image = main_image

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

def products_all_view(request):
    products = Product.objects.all().order_by('-created_at')
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    categories = Category.objects.all()

    wishlist_product_ids = []
    if request.user.is_authenticated:
        if hasattr(request.user, 'wishlist'):
            wishlist_product_ids = request.user.wishlist.products.values_list('id', flat=True)
        else:
            wishlist_product_ids = []

    context = {
        'products': products,
        'categories': categories,
        'wishlist_product_ids': wishlist_product_ids,
        'search_query': query,
    }

    return render(request, 'products_all.html', context)


from decimal import Decimal  # BU YERGA IMPORT QO'SHING


def add_product(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        # FLOAT emas, DECIMAL ishlatamiz:
        try:
            price = Decimal(request.POST.get('price', '0'))
            precent = int(request.POST.get('precent', 0))
            stock = int(request.POST.get('stock', 1))
        except (ValueError, TypeError, Decimal.InvalidOperation):
            price = Decimal('0')
            precent = 0
            stock = 1

        category_id = request.POST.get('category')
        main_image = request.FILES.get('main_image')
        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            title=title,
            description=description,
            price=price,
            precent=precent,
            stock=stock,
            main_image=main_image,
            category=category,
            seller=request.user,
        )
        return redirect('products_all')  # Yoki o'zingiz istagan sahifa

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})

