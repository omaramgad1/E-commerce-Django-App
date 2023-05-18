from django.db import models
from product.models import Product
from django.db import models
from user_app.models import User
# Create your models here.


class OrderList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s OrderList"


class Order(models.Model):
    orderList = models.ForeignKey(
        OrderList, on_delete=models.CASCADE, related_name="orders")
    # items = models.ManyToManyField(Product, through='OrderItem')
    shipping_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('credit', 'Credit Card'),
        ('cod', 'Cash on Delivery'),
    ])

    payment_method = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ])

    def __str__(self) -> str:
        return f"{self.orderList.user.username}'s {self.pk} - Order"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderItems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=7)
    color = models.CharField(max_length=7)

    def __str__(self) -> str:
        return f"{self.order.orderList.user.username}'s {self.product.name} - {self.size} - {self.color}"


class PaymentToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ptoken = models.CharField(max_length=32)
    status = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Payment Token"
