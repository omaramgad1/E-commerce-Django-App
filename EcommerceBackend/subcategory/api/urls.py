from django.urls import path
from .views import *


urlpatterns = [
    path('', SubCategory_pagenation, name='SubCategory_pagenation'),
    path('list/', SubCategory_list, name='SubCategory_list'),
    path('create/', SubCategory_Create, name='SubCategory_Create'),
    path('update/<int:pk>/', SubCategory_update, name='SubCategory_update'),
    path('delete/<int:pk>/', SubCategory_delete, name='SubCategory_delete'),
    path('<int:pk>/', SubCategory_details, name='subcategory_details'),
    path('<int:pk>/products/', SubCategory_Products, name='SubCategory_Products'),

]
