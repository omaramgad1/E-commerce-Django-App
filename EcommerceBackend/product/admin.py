from django.contrib import admin

from .models import Product, ProductDetails
admin.site.register(Product)
admin.site.register(ProductDetails)
