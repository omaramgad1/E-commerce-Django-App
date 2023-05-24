from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user_app.api.urls')),
    path('category/', include('category.api.urls')),
    path('subcategory/', include('subcategory.api.urls')),
    path('product/', include('product.api.urls')),
    path('wishlist/', include('wishlist.api.urls')),
    path('cart/', include('cartlist.api.urls')),
    path('order/', include('orderlist.api.urls')),
    path('swagger/doc', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    # path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += staticfiles_urlpatterns()
