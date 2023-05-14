from rest_framework import serializers
from ..models import OrderList, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_total(self, obj):
        return sum(item.quantity * item.product.price for item in obj.order_items.all())


class OrderListSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrderList
        fields = '__all__'
