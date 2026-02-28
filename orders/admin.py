from django.contrib import admin

from .models import *

admin.site.register([Order,OrderItem])
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]