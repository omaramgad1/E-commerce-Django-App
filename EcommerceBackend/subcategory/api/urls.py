from django.urls import path
from .views import *


urlpatterns = [
    path('', SubCategory_list, name='subcategory_list'),
    path('<int:pk>/', SubCategory_details, name='subcategory_details'),
]
