from django.urls import path
from .views import *


urlpatterns = [
    path('', Category_pagenation, name='Category_pagenation'),
    path('list/', Category_list, name='category_list'),
    path('create/', Category_Create, name='Category_Create'),
    path('update/<int:pk>/', Category_Update, name='Category_Update'),
    path('delete/<int:pk>/', Category_Delete, name='Category_Delete'),
    path('<int:pk>/', Category_details, name='Category_details'),
    path('<int:pk>/subcategories/',
         Category_subcategories, name='Category_subcategories'),

    path('<int:pk>/products/', Category_Products, name='Category_Products'),


]
