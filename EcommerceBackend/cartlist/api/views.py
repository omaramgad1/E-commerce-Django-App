from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.models import User
from product.models import Product, Inventory
from ..models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = get_object_or_404(User, id=request.user.id)
    cart = Cart.objects.get(user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsOwner])
def get_cart_item(request, item_id):
    user = get_object_or_404(User, id=request.user.id)
    item = get_object_or_404(CartItem, id=item_id, cart__user=user)
    serializer = CartItemSerializer(item)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_item(request, product_id):

    cart = Cart.objects.get(user=request.user)

    try:
        # Get the product and inventory item
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # Get the inventory object
        message = "This product does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    color = request.POST.get('color')
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity'))
    try:
        inventory = Inventory.objects.get(
            product=product, color=color, sizes=size)
    except Inventory.DoesNotExist:
        message = "This product has no inventory"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    if inventory.quantity < quantity:
        message = f"Sorry, there's not enough inventory for this product with color {color} and size {size}."
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    cart = Cart.objects.get(user=request.user)
    serailzer = CartSerializer(cart)

    matching_items = [item for item in serailzer.data['cartItems']
                      if item['product'] == product.id and
                      item['color'] == color and
                      item['size'] == size]

    if matching_items:
        return Response({'error': "This product is already in your cart"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Create a new cart item and add it to the cart
    cart_item = CartItem.objects.create(
        cart=cart, product=product, size=size, color=color, quantity=quantity)

    cart_item.save()

    # Return a JSON response indicating success
    return Response({'message': "Added To Your Cart successfully"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsOwner])
def update_cart_item(request, item_id):
    # Get the product and inventory item
    try:
        # Get the product and inventory item
        cart_item = CartItem.objects.get(pk=item_id)
        inventory_item = Inventory.objects.get(
            product=cart_item.product, color=cart_item.color, sizes=cart_item.size)
    except CartItem.DoesNotExist:
        # Get the inventory object
        message = "This cart_item does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    except Inventory.DoesNotExist:
        message = "This Inventory does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    # cart_item = get_object_or_404(CartItem, pk=item_id)

    # inventory_item = get_object_or_404(
    #     Inventory, product=cart_item.product, color=cart_item.color, sizes=cart_item.size)
    new_quantity = int(request.data.get('quantity'))
    if inventory_item.quantity < new_quantity:
        message = f"Sorry, there's not enough inventory for this product with color {cart_item.color} and size {cart_item.size}."
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

    # Get the user's cart or create a new one if it doesn't exist
    # cart = Cart.objects.get(user=request.user)

    # Create a new cart item and add it to the cart
    cart_item.quantity = new_quantity
    cart_item.save()

    # Return a JSON response indicating success
    return Response({'message': "Updated cart item successfully"})


@api_view(['DELETE'])
@permission_classes([IsOwner])
def remove_item_from_cart(request, item_id):
    user = get_object_or_404(User, id=request.user.id)
    item = get_object_or_404(CartItem, id=item_id)
    cart = get_object_or_404(Cart, user=user)

    serializer = CartSerializer(cart)
    serializer2 = CartItemSerializer(item)

    print(serializer2.data not in serializer.data['cartItems'])

    if serializer2.data not in serializer.data['cartItems']:
        return Response({'error': 'This item is not in your cart.'}, status=400)

    item.delete()
    serializer = CartSerializer(cart)
    return Response({'message': "Delete From Cart successfuly"}, status=status.HTTP_200_OK)
