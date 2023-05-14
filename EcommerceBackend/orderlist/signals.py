from user_app.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderList


@receiver(post_save, sender=User)
def create_orderlist(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        OrderList.objects.create(user=instance)
