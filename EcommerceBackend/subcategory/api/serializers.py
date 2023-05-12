from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import serializers
from ..models import SubCategory
from category.models import Category
from product.api.serializers import ProductSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

    def create(self, validated_data):
        category_name = validated_data.pop('category')['name']
        category = Category.objects.get(name=category_name)
        subcategory = SubCategory.objects.create(
            category=category, **validated_data)
        return subcategory

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', {}).get('name')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                instance.category = category
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'error':
                                                   "Category with name %s does not exist" % category_name})  # 400 bad request
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
