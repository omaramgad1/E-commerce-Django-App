from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import serializers
from ..models import SubCategory
from category.models import Category
from product.api.serializers import ProductSerializer
from django.db import IntegrityError


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

    # def create(self, validated_data):
    #     category_name = validated_data.pop('category')['name']
    #     category = Category.objects.get(name=category_name)
    #     subcategory = SubCategory.objects.create(
    #         category=category, **validated_data)
    #     return subcategory
    def create(self, validated_data):
        try:
            category_name = validated_data.pop('category')['name']
            category = Category.objects.get(name=category_name)
            subcategory = SubCategory.objects.create(
                category=category, **validated_data)
        except IntegrityError:
            message = f"A subcategory with name '{validated_data['name']}' already exists in category '{category_name}'."
            raise serializers.ValidationError({'error': message})
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'error':
                                               "Category with name %s does not exist" % category_name})
        return subcategory

    # def update(self, instance, validated_data):
    #     category_name = validated_data.pop('category', {}).get('name')
    #     if category_name:
    #         try:
    #             category = Category.objects.get(name=category_name)
    #             instance.category = category
    #         except IntegrityError:
    #             message = f"A subcategory with name '{validated_data['name']}' already exists in category '{category_name}'."
    #             raise serializers.ValidationError({'error': message})
    #         except ObjectDoesNotExist:
    #             raise serializers.ValidationError({'error':
    #                                                "Category with name %s does not exist" % category_name})  # 400 bad request
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()

    #     return instance
    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', {}).get('name')

        if category_name:

            try:

                category = Category.objects.get(name=category_name)
                instance.category = category
            except IntegrityError:
                message = f"A subcategory with name '{validated_data['name']}' already exists in category '{category_name}'."
                raise serializers.ValidationError({'error': message})
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'error':
                                                   "Category with name %s does not exist" % category_name})  # 400 bad request
        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
        except IntegrityError:
            message = f"A subcategory with name '{validated_data['name']}' already exists in category '{category_name}'."
            raise serializers.ValidationError({'error': message})

        return instance
