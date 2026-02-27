from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Review


# 1. Izoh qo'shish
def add_review(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Agar bir nechta komment yozishga ruxsat bermoqchi bo'lsangiz,
        # filter(...).exists() tekshiruvini olib tashlaymiz.
        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi!")
        return redirect('product_detail', pk=product.id)

    return redirect('product_detail', pk=product_id)


# 2. Izohni o'chirish
def delete_review(request, review_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Faqat o'ziga tegishli reviewni o'chira oladi
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()

    messages.info(request, "Izohingiz o'chirildi.")
    return redirect('product_detail', pk=product_id)


def edit_review(request, review_id):
    if not request.user.is_authenticated:
        return redirect('login')

    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        review.save()

        messages.success(request, "Izohingiz yangilandi.")
        return redirect('product_detail', pk=review.product.id)

    return redirect('product_detail', pk=review.product.id)