from django.urls import path
from . import views

app_name = 'reviews'  # Mana bu satr juda muhim

urlpatterns = [
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
]