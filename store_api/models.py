from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="Smartphones & Gadgets")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=15)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.brand} {self.name} (₱{self.price})"