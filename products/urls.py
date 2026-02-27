from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('my-products/', views.my_products_view, name='my_products'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/edit/<int:pk>/', views.product_edit_view, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete_view, name='product_delete'),
    path('products/', views.products_all_view, name='products_all'),
]