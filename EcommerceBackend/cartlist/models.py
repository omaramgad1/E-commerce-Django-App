from product.models import Product
from django.db import models
from user_app.models import User
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Product,through='CartItem')
    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartItems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=7)
    color = models.CharField(max_length=7)
    
    def __str__(self) -> str:
        return f"{self.cart.user.username}'s {self.product.name} - {self.size} - {self.color}"