from django.contrib import admin
from .models import OrderList, Order, OrderItem, PaymentToken


class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderList', 'id', 'created_at',
                    'delivered_time', 'shipped_time', 'status', 'shipping_address')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'orderList__user__username', 'shipping_address')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'size', 'color')
    list_filter = ('order__orderList__user',
                   'product__subcategory__category', 'product__subcategory')
    search_fields = ('order__orderList__user__username',
                     'product__name', 'size', 'color')


admin.site.register(OrderList)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(PaymentToken)
