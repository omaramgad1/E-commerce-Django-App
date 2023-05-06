from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from .serializers import CategorySerializer
from django.core.paginator import Paginator

# page = request.GET.get('page', 1)
# paginator = Paginator(queryset, limit)
# objects = paginator.get_page(page)


@api_view(['GET'])
def Category_pagenation(request):
    if request.method == 'GET':
        queryset = Category.objects.all()
        queryset_len = Category.objects.all().count()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)

        paginator = Paginator(queryset, limit)
        objects = paginator.get_page(page)
        serializer = CategorySerializer(objects, many=True)
        return Response({'data': serializer.data,
                         'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                         'current_page': objects.number,
                         'next_page': objects.next_page_number() if objects.has_next() else None,
                         'total_Docs': queryset_len,
                         'total_pages': paginator.num_pages,
                         })


@api_view(['GET', 'POST'])
def Category_list(request):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'data': serializer.data})

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Created Successfuly'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT', 'DELETE'])
def Category_details(request, pk):

    if request.method == 'GET':

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response({'data': serializer.data})

    if request.method == 'PUT':
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category Upateded Successfuly'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)

        if serializer.data['subcategories'] != []:
            return Response({'error': 'Category Has SubCategories '}, status=status.HTTP_406_NOT_ACCEPTABLE)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
