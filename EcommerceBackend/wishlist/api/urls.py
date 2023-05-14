from django.urls import path
from .views import *


urlpatterns = [
    path('list/', get_wishlist,
         name='get_wishlist'),
    path('add_product/<int:product_id>/', add_product_to_wishlist,
         name='add_product_to_wishlist'),
    path('delete_product/<int:product_id>/', remove_product_from_wishlist,
         name='remove_product_from_wishlist'),
]
