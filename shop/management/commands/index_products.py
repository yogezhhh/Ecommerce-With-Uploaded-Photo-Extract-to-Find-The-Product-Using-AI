from django.core.management.base import BaseCommand
from PIL import Image
from shop.models import Product
from shop.lens_engine import embed_image


class Command(BaseCommand):
    help = "Generate CLIP embeddings for products without one"

    def handle(self, *args, **kw):
        qs = Product.objects.filter(embedding__isnull=True).exclude(image='')
        self.stdout.write(f"Indexing {qs.count()} product(s)...")
        for p in qs:
            try:
                img = Image.open(p.image.path).convert('RGB')
                p.embedding = embed_image(img).tobytes()
                p.save(update_fields=['embedding'])
                self.stdout.write(self.style.SUCCESS(f"  ✓ {p.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ {p.name}: {e}"))
        self.stdout.write(self.style.SUCCESS("Done."))