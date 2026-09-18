from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    embedding = models.BinaryField(null=True, blank=True)  # AI feature vector
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name