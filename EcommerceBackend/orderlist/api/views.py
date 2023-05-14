from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.models import User
from product.models import Product, Inventory
from ..models import Order, OrderList, OrderItem, PaymentToken
from .serializers import OrderItemSerializer, OrderSerializer, OrderListSerializer
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsOwner
from cartlist.models import Cart, CartItem
import stripe
import secrets
from django.conf import settings
from django.shortcuts import redirect
from stripe.error import AuthenticationError
from rest_framework.permissions import IsAdminUser, AllowAny
# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@permission_classes(['IsOwner'])
def create_Checkout(request):
    user = User.objects.get(id=request.user.id)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    payment_method = request.data.get('payment_method')
    shipping_address = request.data.get('shipping_address')
    base_url = request.scheme + '://' + request.get_host()
    # validation before checkout
    if not cart_items:
        return Response({"error": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
    for cart_item in cart_items:
        inventory = Inventory.objects.get(
            product=cart_item.product,
            color=cart_item.color,
            size=cart_item.size,
        )
        if not inventory:
            return Response({'error': f"Inventory not Found"}, status=status.HTTP_400_BAD_REQUEST)
        if cart_item.quantity > inventory.quantity:
            return Response({'error': f"Sorry, we do not have enough stock for {cart_item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)

    if payment_method == 'cod':
        return redirect(f'{base_url}/order/create?user={user.id}&method={payment_method}&address={shipping_address}', code=303)
    elif payment_method == 'credit':
        line_items = []
        for item in cart_items:
            product_name = item.product.name
            price = item.product.price * 100  # Stripe requires the price in cents
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(price)
                },
                'quantity': item.quantity
            }
            line_items.append(line_item)
        try:
            token = secrets.token_hex(16)
            base_url = request.scheme + '://' + request.get_host()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f'{base_url}/order/create?token={token}&user={user.id}&session_id={{CHECKOUT_SESSION_ID}}&method={payment_method}&address={shipping_address}',
                cancel_url=f'{base_url}/order/cancel?token={token}&user={user.id}',
            )
            pToken = PaymentToken(user=user, ptoken=token,
                                  status=True, token=checkout_session.id)
            pToken.save()
        except stripe.error.AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return redirect(checkout_session.url, code=303)


@api_view(['POST'])
def cancel_order(request):
    user_id = request.GET.get('user')
    token = request.GET.get('token')
    try:
        pToken = PaymentToken.objects.get(
            user_id=user_id, ptoken=token, status=True)
        checkout_session = stripe.checkout.Session.retrieve(pToken.token)
        checkout_session.cancel()
        pToken.status = False
        pToken.save()
    except PaymentToken.DoesNotExist:
        return Response({'error': 'Invalid payment token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Order cancelled successfully'})


@api_view(['POST'])
def create_order(request):
    user_id = request.GET.get('user')
    token = request.GET.get('token')
    session_id = request.GET.get('session_id')
    payment_method = request.get('method')
    shipping_address = request.get('address')

    with transaction.atomic():
        if payment_method == 'cod' and not token:
            pass
        elif payment_method == 'credit' and token:
            pToken = PaymentToken.objects.get(
                user=user, Ptoken=token, token=session_id, status=True)

            if not pToken:
                return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
            pToken.status = False
            pToken.save()
        else:
            return Response({"error": "Unvaild Payment Method !!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
        # cart_items = CartItem.objects.filter(cart=cart)

        # Get the user's order list
        order_list = OrderList.objects.get(user=user)

        # Create the order
        order = Order.objects.create(
            orderList=order_list,
            shipping_address=shipping_address,
            status='pending',
            payment_method=payment_method,
        )

        # Loop through the cart items and create order items
        for cart_item in cart.items.all():
            # Get the inventory object for the product, color, and size
            inventory = Inventory.objects.get(
                product=cart_item.product,
                color=cart_item.color,
                size=cart_item.size,
            )
            if not inventory:
                return Response({'error': f"Inventory not Found"}, status=status.HTTP_400_BAD_REQUEST)
            if cart_item.quantity > inventory.quantity:
                return Response({'error': f"Sorry, we do not have enough stock for {cart_item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
            # Update the inventory quantity and save
            inventory.quantity -= cart_item.quantity
            inventory.save()

            # Create the order item
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                color=cart_item.color,
                size=cart_item.size,
                quantity=cart_item.quantity,
            )

            # Delete the cart item
            cart_item.delete()

        # Add the order to the user's order list and save
        order_list.orders.add(order)
        order_list.save()
    # Serialize and return the updated cart
    return Response({'message': "done"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes(['IsOwner'])
def order_details(request, order_id):
    user = User.objects.get(id=request.user.id)
    try:
        orderlist = OrderList.objects.get(user=user)
        order = Order.objects.get(orderlist=orderlist, id=order_id)
        order_items = order.items.all()
        serialized_order_items = OrderItemSerializer(
            order_items, many=True).data
        serialized_order = OrderSerializer(order).data
        return Response({'data': {'order': serialized_order,
                                  'items': serialized_order_items}},
                        status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes(['IsOwner'])
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status.lower() == 'pending':
        for order_item in order.items.all():
            inventory = Inventory.objects.get(
                product=order_item.product,
                color=order_item.color,
                size=order_item.size,
            )
            inventory.quantity += order_item.quantity
            order_item.delete()
        order.delete()
        return Response({'data': {'message': 'Order deleted successfully'}}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Cannot delete order with status other than "pending".'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes(['IsOwner'])
def get_orderList(request):
    user = User.objects.get(id=request.user.id)
    orderlist = OrderList.objects.get(user=user)
    serialized_orderlist = OrderListSerializer(orderlist).data
    return Response({'data': serialized_orderlist}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id):
    status = request.data.get('status')
    if status.lower() not in ['pending', 'shipped', 'delivered']:
        return Response({'error': 'Invalid Status'}, status=status.HTTP_400_BAD_REQUEST)
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return Response({'message': 'Order Status Changed to {status}'}, status=status.HTTP_200_OK)
