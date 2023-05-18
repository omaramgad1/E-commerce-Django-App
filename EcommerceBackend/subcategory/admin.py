from django.contrib import admin

# Register your models here.
from .models import SubCategory


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


admin.site.register(SubCategory, SubCategoryAdmin)
