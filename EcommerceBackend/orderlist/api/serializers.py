from rest_framework import serializers
from ..models import OrderList, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image_url = serializers.ImageField(
        source='product.imageUrl', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'product_name', 'product_price',
                  'product_image_url', 'quantity', 'size', 'color', 'total')

    def get_total(self, obj):
        """
        Calculate the total price for the order item based on its quantity and product price.
        """
        return obj.quantity * obj.product.price


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='orderList.user.username')

    class Meta:
        model = Order
        fields = ('username', 'total', 'orderItems',)  # '__all__'
        # exclude = ('items',)

    def get_total(self, obj):
        return sum(item.quantity * item.product.price for item in obj.orderItems.all())


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrderList
        fields = '__all__'
