from django.urls import path
from .views import *


urlpatterns = [
    path('checkout/', create_Checkout, name="create_checkout"),
    path('create/<str:token>/<int:user_id>/<str:session_id>/<str:method>/<str:address>/',
         create_order, name='create_Checkout'),
    path('cancel/<str:token>/<int:user_id>/',
         cancel_order, name="cancel_order"),
    path('details/<int:order_id>/', order_details, name="get_order_details"),
    path('delete/<int:order_id>/', delete_order, name="delete_order"),
    path('list/', get_orderList, name="get_order_list"),
    path('list_orders/', get_orders, name="get_orders"),

    path('updateStatus/<int:order_id>/',
         update_order_status, name="update_order_status"),
    path('all/', get_all_orders, name="get_all_orders"),
    path('all_search/', OrderSearchView.as_view(), name="OrderSearchView"),


]
