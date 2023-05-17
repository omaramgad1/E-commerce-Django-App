from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user_app.api.urls')),
    path('category/', include('category.api.urls')),
    path('subcategory/', include('subcategory.api.urls')),
    path('product/', include('product.api.urls')),
    path('wishlist/', include('wishlist.api.urls')),
    path('cart/', include('cartlist.api.urls')),
    path('order/', include('orderlist.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]
