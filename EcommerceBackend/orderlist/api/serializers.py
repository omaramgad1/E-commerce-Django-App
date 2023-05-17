from rest_framework import serializers
from ..models import OrderList, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ('items',)

    def get_total(self, obj):
        return sum(item.quantity * item.product.price for item in obj.orderItems.all())


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrderList
        fields = '__all__'
