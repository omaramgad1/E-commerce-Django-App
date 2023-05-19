from django.db import models
from subcategory.models import SubCategory
from category.models import Category

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
        return self.name+"_"+self.subcategory.name+"_"+self.subcategory.category.name


class Inventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='inventory')
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    size = models.CharField(max_length=3, choices=[
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ])

    class Meta:
        verbose_name_plural = 'Inventories'
        # Add a unique constraint on the `color` and `sizes` fields
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'], name='unique_color_size')
        ]

    def __str__(self):
        return self.product.name+"_"+self.product.subcategory.name+"_"+self.product.subcategory.category.name + "_Inventory_" + str(self.pk)

    def save(self, *args, **kwargs):
        self.color = self.color.strip().replace(" ", "_").lower()
        super(Inventory, self).save(*args, **kwargs)
