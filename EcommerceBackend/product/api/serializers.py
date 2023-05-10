from rest_framework import serializers
from ..models import Product, Inventory
from subcategory.models import SubCategory


class InventorySerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = Inventory
        fields = '__all__'  # ('color', 'sizes', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name')
    inventory = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'  # ('id', 'name', 'description', 'imageUrl',
        # 'price', 'subcategory', 'details')

    def create(self, validated_data):
        subcategory_name = validated_data.pop('subcategory')['name']
        subcategory, _ = SubCategory.objects.get_or_create(
            name=subcategory_name)
        product = Product.objects.create(
            subcategory=subcategory, **validated_data)
        return product
