from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import WishList
from product.models import Product
from .serializers import WishListSerializer
from .permissions import IsOwner
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsOwner])
def add_product_to_wishlist(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not Found.'}, status=status.HTTP_404_NOT_FOUND)

    wishlist = WishList.objects.get(user=request.user)
    if product in wishlist.products.all():
        return Response({'error': 'This product is already in your wishlist.'}, status=400)
    wishlist.products.add(product)
    return Response({"message": "Add product to wishlist successfully"})


@api_view(['GET'])
@permission_classes([IsOwner])
def get_wishlist(request):
    wishlist = WishList.objects.get(user=request.user)
    serializer = WishListSerializer(wishlist)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsOwner])
def remove_product_from_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        wishlist = WishList.objects.get(user=request.user)
    except Product.DoesNotExist:
        return Response({'error': 'Product not Found.'}, status=status.HTTP_404_NOT_FOUND)

    except WishList.DoesNotExist:
        return Response({'error': 'WishList not Found.'}, status=status.HTTP_404_NOT_FOUND)

    if product not in wishlist.products.all():
        return Response({'error': 'This product is not in your wishlist.'}, status=400)
    wishlist.products.remove(product)
    serializer = WishListSerializer(wishlist)
    return Response(serializer.data)
