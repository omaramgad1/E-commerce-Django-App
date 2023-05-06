from django.urls import path
from .views import *


urlpatterns = [
    path('list-all', Category_list, name='category_list'),
    path('list', Category_pagenation, name='Category_pagenation'),

    path('<int:pk>/', Category_details, name='Category_details'),
]
