from django.urls import path
from .views import *


urlpatterns = [
    path('', SubCategory_list, name='subcategory_list'),
    path('list-all', SubCategory_list, name='subcategory_list'),
    path('list', SubCategory_pagenation, name='SubCategory_pagenation'),
    path('<int:pk>/', SubCategory_details, name='subcategory_details'),
]
