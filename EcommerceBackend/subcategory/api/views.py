from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import SubCategory
from .serializers import SubCategorySerializer
from django.core.paginator import Paginator
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import permission_classes, renderer_classes


@api_view(['GET'])
@permission_classes([AllowAny])
def SubCategory_pagenation(request):
    if request.method == 'GET':
        queryset = SubCategory.objects.all()
        queryset_len = SubCategory.objects.all().count()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)

        paginator = Paginator(queryset, limit)
        objects = paginator.get_page(page)
        serializer = SubCategorySerializer(objects, many=True)
        return Response({'data': serializer.data,
                         'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                         'current_page': objects.number,
                         'next_page': objects.next_page_number() if objects.has_next() else None,
                         'total_Docs': queryset_len,
                         'total_pages': paginator.num_pages,
                         })


@api_view(['GET'])
@permission_classes([AllowAny])
def SubCategory_list(request):
    if request.method == 'GET':
        categories = SubCategory.objects.all()
        serializer = SubCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def SubCategory_details(request, pk):

    if request.method == 'GET':

        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def SubCategory_Products(request, pk):
    if request.method == 'GET':
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubCategorySerializer(subcategory)
        products = []
        for item in serializer.data['products']:
            products.append(item)
        return Response(products)


@api_view(['POST'])
@permission_classes([AllowAny])
@permission_classes([IsAdminUser])
def SubCategory_Create(request):
    if request.method == 'POST':

        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Subcategory Created Successfuly'}, status=status.HTTP_201_CREATED)
        else:
            # if serializer.errors['category']:
            #     return Response({'error': serializer.errors['category']}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if serializer.errors['name']:
                return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def SubCategory_update(request, pk):
    if request.method == 'PUT':
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Upateded Successfuly'}, status=status.HTTP_200_OK)
        else:
            if serializer.errors['category']:
                return Response({'error': serializer.errors['category']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif serializer.errors['name']:
                return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def SubCategory_delete(request, pk):
    if request.method == 'PUT':
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Upateded Successfuly'}, status=status.HTTP_200_OK)
        else:
            if serializer.errors['category']:
                return Response({'error': serializer.errors['category']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif serializer.errors['name']:
                return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == 'DELETE':
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubCategorySerializer(subcategory)

        if serializer.data['products'] != []:
            return Response({'error': 'subcategory Has products '}, status=status.HTTP_406_NOT_ACCEPTABLE)
        subcategory.delete()
        return Response({"message": "Category Deleted Successfuly"}, status=status.HTTP_200_OK)
