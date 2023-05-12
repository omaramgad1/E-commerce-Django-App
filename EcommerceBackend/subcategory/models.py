from django.db import models
from rest_framework.exceptions import ValidationError
from category.models import Category
from django.db.models import Q
# Create your models here.


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'SubCategories'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'], name='unique_subcategory_name_category')
        ]

    def __str__(self):
        return self.category.name+"_"+self.name
