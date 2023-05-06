from rest_framework import serializers
from ..models import Product, ProductDetails


class ProductDetailSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = ProductDetails
        fields = '__all__'  # ('color', 'sizes', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name')
    details = ProductDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'imageUrl',
                  'price', 'subcategory', 'details')
