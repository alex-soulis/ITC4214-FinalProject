from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'reviews' )
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars)"