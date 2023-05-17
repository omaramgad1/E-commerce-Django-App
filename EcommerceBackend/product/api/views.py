from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Inventory
from .serializers import ProductSerializer, InventorySerializer
from django.core.paginator import Paginator
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db import IntegrityError


@api_view(['GET'])
@permission_classes([AllowAny])
def product_pagenation(request):
    if request.method == 'GET':
        queryset = Product.objects.all()
        queryset_len = Product.objects.all().count()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)

        paginator = Paginator(queryset, limit)
        objects = paginator.get_page(page)
        serializer = ProductSerializer(objects, many=True)
        return Response({'data': serializer.data,
                         'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                         'current_page': objects.number,
                         'next_page': objects.next_page_number() if objects.has_next() else None,
                         'total_Docs': queryset_len,
                         'total_pages': paginator.num_pages,
                         })


@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_details(request, pk):
    if request.method == 'GET':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product Created Successfuly'}, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            for field, message in serializer.errors.items():
                errors[field] = message[0]
            return Response({'error': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def product_update(request, pk):

    if request.method == 'PUT':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product Upateded Successfuly'}, status=status.HTTP_200_OK)
        else:
            errors = {}
            for field, message in serializer.errors.items():
                errors[field] = message[0]
            return Response({'error': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def product_delete(request, pk):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'message': "Product Deleted Successfully"}, status=status.HTTP_200_OK)


#################################### inventory #########################
@api_view(['GET'])  # not  used for testing purposes
@permission_classes([AllowAny])
def get_inventories(request):
    if request.method == 'GET':
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_inventory(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        inventory = Inventory.objects.filter(product=product)
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_inventory_colors_for_product(request, product_id):
    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    colors = Inventory.objects.filter(
        product_id=product_id).values_list('color', flat=True).distinct()
    return Response({'colors': colors}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_inventory_sizes_for_product(request, product_id):
    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    sizes = Inventory.objects.filter(product_id=product_id).values_list(
        'sizes', flat=True).distinct()
    return Response({'sizes': sizes}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_sizes_for_product_and_color(request, product_id, color):

    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    colors = Inventory.objects.filter(
        product_id=product_id).values_list('color', flat=True).distinct()

    color = color.replace(' ', '').strip().lower()

    if color in [c.strip().lower() for c in colors]:
        inventory = Inventory.objects.filter(
            product_id=product_id, color=color)
    else:
        return Response({'error': 'Product color not found'}, status=status.HTTP_404_NOT_FOUND)

    sizes = set(inventory.values_list('sizes', flat=True))
    return Response({'sizes': list(sizes)})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_quantity_for_product_color_and_size(request, product_id, color, size):

    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    colors = Inventory.objects.filter(
        product_id=product_id).values_list('color', flat=True).distinct()
    sizes = Inventory.objects.filter(product_id=product_id).values_list(
        'sizes', flat=True).distinct()

    color = color.replace(' ', '').strip().lower()
    size = size.replace(' ', '').strip().upper()

    if color in [c.strip().lower() for c in colors]:
        if size in [s.strip().upper() for s in sizes]:
            inventory = Inventory.objects.filter(
                product_id=product_id, color=color, sizes=size.upper())
            quantity = sum([inv.quantity for inv in inventory])
            return Response({'quantity': quantity})
        else:
            return Response({'error': 'Product size not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Product color not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_inventory_to_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventorySerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            message = f"A inventory with color : '{serializer.validated_data['color']}' and size '{serializer.validated_data['sizes']}' already exists for product '{product.name}'."
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        errors = {}
        for field, message in serializer.errors.items():
            errors[field] = message[0]
        return Response({'error': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_inventory_for_product(request, product_id, inventory_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        inventory = Inventory.objects.get(id=inventory_id, product=product)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventorySerializer(
        inventory, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            message = f"A inventory with color : '{serializer.validated_data['color']}' and size '{serializer.validated_data['sizes']}' already exists for product '{product.name}'."
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        errors = {}
        for field, message in serializer.errors.items():
            errors[field] = message[0]
        return Response({'error': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_inventory_for_product(request, product_id, inventory_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        inventory = Inventory.objects.get(id=inventory_id, product=product)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    inventory.delete()
    return Response({'messagge': 'Inventory deleted'}, status=status.HTTP_204_NO_CONTENT)
