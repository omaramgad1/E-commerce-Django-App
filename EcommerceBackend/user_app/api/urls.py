from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [


    path('register/', register, name='register'),
    path('login/', login, name='login'),

    path('profile/', profile_get, name='profile'),
    path('profile_update/', profile_update, name='profile_update'),
    path('change_password/', change_password, name='change_password'),
    path('list/', get_users_pagination, name='get_users_pagination'),
    path('list-all/', get_all_users, name='get_all_users'),
    path('list-active/', get_active_users, name='get_active_users'),
    path('list-admins/', get_superusers_users, name='get_superusers_users'),

    # path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    # path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path('<int:user_id>/change_active_status/',
         change_user_active_status, name='change_user_active_status'),
    path('<int:user_id>/',
         get_user_details, name='get_user_details'),



    path('<int:user_id>/change_to_admin/', change_user_superuser_status,
         name='change_user_superuser_status'),

    # path('forgot_password/', forgot_password, name='forgot_password'),
    # path('reset_password/', reset_password, name='reset_password'),

]
