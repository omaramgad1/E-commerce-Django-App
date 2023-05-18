from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)
    inlines = [CartItemInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'size', 'color')
    list_filter = ('cart__user__username', 'product__subcategory__category',
                   'product__subcategory')
    search_fields = ('cart__user__username', 'product__name', 'size', 'color')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
