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
    try:
        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=user)
    except User.DoesNotExist:
        return Response({'error': "User not Found"}, status=status.HTTP_404_NOT_FOUND)

    except Cart.DoesNotExist:
        return Response({'error': "Cart not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsOwner])
def get_cart_item(request, item_id):
    try:
        user = User.objects.get(id=request.user.id)
        item = CartItem.objects.get(id=item_id, cart__user=user)
    except User.DoesNotExist:
        return Response({'error': "User not Found"}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({'error': "Cart Item not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(item)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_item(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({'error': "Cart not Found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Get the product and inventory item
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # Get the inventory object
        message = "This product does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    color = request.POST.get('color')
    size = request.POST.get('size')
    quantity = request.POST.get('quantity')
    if color and size and quantity:
        color = color.strip().replace(' ', '_').lower()
        size = size.strip().replace(' ', '').upper()
        quantity = int(request.POST.get('quantity'))

    else:
        return Response({'error': "Please fill in all fields ( color , size ,  quantity)"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        inventory = Inventory.objects.get(
            product=product, color=color, size=size)
    except Inventory.DoesNotExist:
        message = f"This product has no inventory with that color {color} and size {size}"
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
    serializer = CartItemSerializer(cart_item)

    # Return a JSON response indicating success
    return Response({'message': "Added To Your Cart successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsOwner])
def update_cart_item_quantity(request, item_id):
    # Get the product and inventory item
    try:
        # Get the product and inventory item
        cart_item = CartItem.objects.get(pk=item_id)
        inventory_item = Inventory.objects.get(
            product=cart_item.product, color=cart_item.color, size=cart_item.size)
    except CartItem.DoesNotExist:
        # Get the inventory object
        message = "This cart_item does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    except Inventory.DoesNotExist:
        message = "This Inventory does not exist"
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    new_quantity = request.data.get('quantity')

    if new_quantity:
        new_quantity = int(request.data.get('quantity'))
    else:
        return Response({'error': "Please Enter the new quantity"}, status=status.HTTP_400_BAD_REQUEST)

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

    try:
        user = User.objects.get(id=request.user.id)
        item = CartItem.objects.get(id=item_id)
        cart = Cart.objects.get(user=user)
    except User.DoesNotExist:
        return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({'error': 'CartItem does not exist'}, status=status.HTTP_404_NOT_FOUND)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)
    serializer2 = CartItemSerializer(item)

    print(serializer2.data not in serializer.data['cartItems'])

    if serializer2.data not in serializer.data['cartItems']:
        return Response({'error': 'This item is not in your cart.'}, status=400)

    item.delete()
    # serializer = CartSerializer(cart)
    return Response({'message': "Delete From Cart successfuly"}, status=status.HTTP_200_OK)
