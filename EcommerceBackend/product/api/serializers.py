from rest_framework import serializers
from ..models import Product, Inventory
from subcategory.models import SubCategory
from category.models import Category


class InventorySerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'  # ('color', 'sizes', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name')
    parent_category = serializers.CharField(
        source='subcategory.category.name')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        subcategory_name = validated_data.pop('subcategory')
        parent_category = subcategory_name['category']['name']
        # Look up the parent category by name

        parent_category = Category.objects.get(
            name=parent_category)
        # Look up the subcategory by name and parent category
        subcategory = SubCategory.objects.get(
            name=subcategory_name['name'], category=parent_category)

        validated_data['subcategory'] = subcategory
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        subcategory_data = validated_data.pop('subcategory', None)
        parent_category_name = subcategory_data['category']['name']

        # Update the fields on the product instance
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update the subcategory if provided
        if subcategory_data:
            subcategory_name = subcategory_data.get('name')
            if subcategory_name:
                # Look up the subcategory by name and parent category
                subcategory, _ = SubCategory.objects.get_or_create(
                    name=subcategory_name, category=instance.subcategory.category)
                instance.subcategory = subcategory

        # Update the parent category if provxided
        if parent_category_name:
            # Look up the parent category by name
            parent_category, _ = Category.objects.get_or_create(
                name=parent_category_name)
            instance.subcategory.category = parent_category

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance
