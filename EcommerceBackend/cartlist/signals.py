from user_app.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Cart.objects.create(user=instance)
