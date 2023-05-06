from django.db import models
from subcategory.models import SubCategory
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    imageUrl = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="products")

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductDetails(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='details')
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    sizes = models.CharField(max_length=3, choices=[
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ])

    class Meta:
        verbose_name_plural = 'ProductDetails'
