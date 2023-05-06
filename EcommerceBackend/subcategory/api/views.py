from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import SubCategory
from .serializers import SubCategorySerializer


@api_view(['GET', 'POST'])
def SubCategory_list(request):

    if request.method == 'GET':
        categories = SubCategory.objects.all()
        serializer = SubCategorySerializer(categories, many=True)
        return Response({'data': serializer.data})

    if request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Subcategory Created Successfuly'}, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors['category']:
                return Response({'error': serializer.errors['category']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif serializer.errors['name']:
                return Response({'error': serializer.errors['name']}, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT', 'DELETE'])
def SubCategory_details(request, pk):

    if request.method == 'GET':

        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory)
        return Response({'data': serializer.data})

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
        return Response(status=status.HTTP_204_NO_CONTENT)
