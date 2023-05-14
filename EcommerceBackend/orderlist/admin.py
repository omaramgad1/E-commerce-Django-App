from django.contrib import admin
from .models import OrderList, Order, OrderItem

admin.site.register(OrderList)
admin.site.register(Order)
admin.site.register(OrderItem)
