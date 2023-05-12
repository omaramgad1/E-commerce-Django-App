from user_app.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WishList


@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        WishList.objects.create(user=instance)
