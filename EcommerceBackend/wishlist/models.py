from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from user_app.models import User


class WishList(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wishlist', blank=True)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

    class Meta:
        verbose_name_plural = 'wishlists'
