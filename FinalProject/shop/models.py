from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length = 100)
    parent = models.ForeignKey(
        'self',
        null = True, blank = True,
        on_delete = models.CASCADE,
        related_name = 'children'
    )

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    brand = models.CharField(max_length = 100)
    color = models.CharField(max_length = 50)
    size = models.CharField(max_length = 50, blank = True, null = True)
    image = models.ImageField(upload_to = 'products/', blank = True, null = True)
    stock = models.PositiveIntegerField(default = 0)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products')

    def __str__(self):
        return self.name