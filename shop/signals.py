from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from .models import Product
from .lens_engine import embed_image


@receiver(post_save, sender=Product)
def generate_embedding(sender, instance, created, **kwargs):
    if not instance.embedding and instance.image:
        try:
            img = Image.open(instance.image.path).convert("RGB")
            instance.embedding = embed_image(img).tobytes()
            instance.save(update_fields=['embedding'])
        except Exception as e:
            print(f"Embedding failed for {instance.name}: {e}")