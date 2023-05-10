from django.contrib import admin

from .models import Product, Inventory
admin.site.register(Product)
admin.site.register(Inventory)
