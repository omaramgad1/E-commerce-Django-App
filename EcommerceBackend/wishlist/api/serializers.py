from rest_framework import serializers
from ..models import WishList
from product.api.serializers import ProductSerializer


class WishListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = WishList
        fields = ['id', 'user', 'products']
