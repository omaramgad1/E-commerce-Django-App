from .models import Product, Inventory
from django.contrib import admin


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'quantity')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__name', 'color', 'size')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',  'description', 'subcategory',
                    'price')
    list_filter = ('subcategory',)
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
