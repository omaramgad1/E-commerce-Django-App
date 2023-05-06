from rest_framework import serializers
from ..models import Category
from subcategory.api.serializers import SubCategorySerializer


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
