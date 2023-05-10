from rest_framework import serializers
from ..models import Category
from subcategory.api.serializers import SubCategorySerializer
from subcategory.models import SubCategory


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True, read_only=True)
    # subcategories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    # def get_subcategories(self, obj):
    #     return SubCategory.objects.filter(category=obj).values('id', 'name')
