from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Inventory
from .serializers import ProductSerializer, InventorySerializer
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET'])
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product Created Successfuly'}, status=status.HTTP_201_CREATED)
        else:
            # return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


# @api_view(['GET', 'PUT', 'DELETE'])
# def Category_details(request, pk):

#     if request.method == 'GET':

#         # try:
#         # category = Product.get_object_or_404(pk=pk)
#         # except Product.DoesNotExist:
#         #     return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
#         category = Product.get_object_or_404(pk=pk)
#         serializer = ProductSerializer(category)
#         return Response({'data': serializer.data})

#     if request.method == 'PUT':
#         # try:
#         #     category = Category.objects.get(pk=pk)
#         # except Category.DoesNotExist:
#         #     return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
#         category = Product.get_object_or_404(pk=pk)
#         serializer = ProductSerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Product Upateded Successfuly'}, status=status.HTTP_200_OK)
#         else:
#             # return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

#     if request.method == 'DELETE':
#         # try:
#         #     category = Category.objects.get(pk=pk)
#         # except Category.DoesNotExist:
#         #     return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

#         category = Product.get_object_or_404(pk=pk)
#         serializer = ProductSerializer(category)

#         # if serializer.data['subcategories'] != []:
#         #     return Response({'error': 'Category Has SubCategories '}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""     if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            variants_data = request.data.get('variants', [])
            for variant_data in variants_data:
                variant_data['product'] = product.id
                variant_serializer = ProductDetailSerializer(data=variant_data)
                if variant_serializer.is_valid():
                    variant_serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400) """


""" @api_view(['GET'])
def retrieve_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data) """

""" 
@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        variants_data = request.data.get('variants', [])
        for variant_data in variants_data:
            variant_data['product'] = product.id
            variant_serializer = ProductVariantSerializer(data=variant_data)
            if variant_serializer.is_valid():
                variant_serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        variants_data = request.data.get('variants', [])
        for variant_data in variants_data:
            variant_id = variant_data.get('id', None)
            if variant_id:
                variant = get_object_or_404(
                    ProductVariant, pk=variant_id, product=product)
                variant_serializer = ProductVariantSerializer(
                    variant, data=variant_data)
                if variant_serializer.is_valid():
                    variant_serializer.save()
            else:
                variant_data['product'] = product.id
                variant_serializer = ProductVariantSerializer(
                    data=variant_data)
                if variant_serializer.is_valid():
                    variant_serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=204)
 """
