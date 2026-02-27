from django.db import models

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from decimal import Decimal

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precent = models.PositiveIntegerField(default=0) # Chegirma foizi
    stock = models.PositiveIntegerField(default=1)
    main_image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.precent > 0:
            discount_amount = (self.price * Decimal(self.precent)) / Decimal(100)
            self.discount_price = self.price - discount_amount
        else:
            self.discount_price = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title