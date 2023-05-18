from django.contrib import admin
from .models import WishList


class WishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)
    filter_horizontal = ('products',)


admin.site.register(WishList, WishListAdmin)
