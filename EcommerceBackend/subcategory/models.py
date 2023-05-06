from django.db import models

from category.models import Category

# Create your models here.


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name
