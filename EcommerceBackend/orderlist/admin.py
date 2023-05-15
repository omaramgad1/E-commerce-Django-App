from django.contrib import admin
from .models import OrderList, Order, OrderItem, PaymentToken

admin.site.register(OrderList)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentToken)

