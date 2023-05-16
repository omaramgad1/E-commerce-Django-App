from django.urls import path
from .views import *


urlpatterns = [
    path('', product_pagenation, name='product_pagenation'),
    path('list/', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('update/<int:pk>/', product_update, name='product_update'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
    path('<int:pk>/', product_details, name='product_details'),


    path('inventory/list/', get_inventories,
         name='get_inventories'),

    path('<int:product_id>/inventory/', get_product_inventory,
         name='get_product_inventory'),

    path('<int:product_id>/add_inventory/',
         add_inventory_to_product, name='get_product_inventory'),

    path('<int:product_id>/update_inventory/<int:inventory_id>/',
         update_inventory_for_product, name='update_inventory_for_product'),

    ##### not used ###
    path('<int:product_id>/delete_inventory/<int:inventory_id>/',
         delete_inventory_for_product, name='delete_inventory_for_products'),

    path('<int:product_id>/inventory/colors/', get_inventory_colors_for_product,
         name='get_inventory_colors_for_product'),

    path('<int:product_id>/inventory/sizes/', get_inventory_sizes_for_product,
         name='get_inventory_sizes_for_product'),

    path('<int:product_id>/inventory/<str:color>/sizes/',
         get_sizes_for_product_and_color,  name='get_sizes_for_product_and_color'),

    path('<int:product_id>/inventory/<str:color>/<str:size>/quantity/',
         get_quantity_for_product_color_and_size,  name='get_quantity_for_product_color_and_size'),
]
