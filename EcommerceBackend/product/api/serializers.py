from rest_framework import serializers
from ..models import Product, ProductDetails


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = ('color', 'size', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name')
    details = ProductDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'imageUrl', 'price',
                  'quantity', 'subcategory', 'details')
