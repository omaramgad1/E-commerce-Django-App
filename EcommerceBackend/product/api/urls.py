from django.urls import path
from .views import *


urlpatterns = [
    path('list-all', product_list, name='category_list'),
    path('create', create_product, name='create_product'),
    # path('<int:pk>/', ProductDetails, name='Category_details'),

    # path('list', Category_pagenation, name='Category_pagenation'),

]
