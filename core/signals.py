from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post

@receiver(pre_delete, sender=Post)
def delete_featured_image(sender, instance, **kwargs):
    if instance.featured_image:
        instance.featured_image.delete(False)