from django.urls import path
from .views import *


urlpatterns = [
    path('list', get_cart, name='get_cart'),
    path('item/create/<int:product_id>', add_cart_item, name="add_cart_item"),
    path('item/update/<int:item_id>', update_cart_item, name="update_cart_item"),
    path('item/remove/<int:item_id>', remove_item_from_cart,
         name="remove_item_from_cart"),
]
