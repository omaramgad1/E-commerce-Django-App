from rest_framework import serializers
from ..models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.CharField(source='cart.id')
    product_name = serializers.CharField(source='product.name')
    product_img = serializers.CharField(source='product.imageUrl')

    price = serializers.DecimalField(
        source='product.price', max_digits=8, decimal_places=2)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity',
                  'size', 'color', 'price', 'product_img', 'subtotal', 'cart']

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username')
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartItems', 'total']

    def get_total(self, obj):
        return sum(item.quantity * item.product.price for item in obj.cartItems.all())
