from rest_framework import serializers
from ..models import Cart, CartItem
from product.models import Inventory


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.CharField(source='cart.id')
    product_name = serializers.CharField(source='product.name')
    product_img = serializers.ImageField(
        source='product.imageUrl', read_only=True)

    price = serializers.DecimalField(
        source='product.price', max_digits=8, decimal_places=2)
    subtotal = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price

    def get_stock(self, obj):
        try:
            inventory = Inventory.objects.get(
                product=obj.product, color=obj.color, size=obj.size)
        except Inventory.DoesNotExist:
            return 0

        return inventory.quantity


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username')
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartItems', 'total']

    def get_total(self, obj):
        return sum(item.quantity * item.product.price for item in obj.cartItems.all())
