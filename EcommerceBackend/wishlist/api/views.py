from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import WishList
from product.models import Product
from .serializers import WishListSerializer
from .permissions import IsOwner
from user_app.models import User


@api_view(['PUT'])
@permission_classes([IsOwner])
def add_product_to_wishlist(request, product_id):
    user = get_object_or_404(User, id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    wishlist = WishList.objects.get(user=user)
    if product in wishlist.products.all():
        return Response({'error': 'This product is already in your wishlist.'}, status=400)
    wishlist.products.add(product)
    serializer = WishListSerializer(wishlist)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsOwner])
def get_wishlist(request):
    user = get_object_or_404(User, id=request.user.id)
    wishlist = WishList.objects.get(user=user)
    serializer = WishListSerializer(wishlist)
    return Response({'data': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsOwner])
def remove_product_from_wishlist(request, product_id):
    user = get_object_or_404(User, id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(WishList, user=user)
    if product not in wishlist.products.all():
        return Response({'error': 'This product is not in your wishlist.'}, status=400)
    wishlist.products.remove(product)
    serializer = WishListSerializer(wishlist)
    return Response(serializer.data)
