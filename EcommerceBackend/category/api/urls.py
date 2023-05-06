from django.urls import path
from .views import *


urlpatterns = [
    path('', Category_list, name='category_list'),
    path('<int:pk>/', Category_details, name='Category_details'),
]
