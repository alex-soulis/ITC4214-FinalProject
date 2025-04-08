from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField (max_length = 100)
    slug = models.SlugField(unique = True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank = True, null = True, related_name='subcategory'
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:category', args = [self.slug])
    
class Product(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='products')
    brand = models.CharField(max_length = 100)
    color = models.CharField(max_length = 50)
    size = models.CharField(max_length = 50, blank = True, null = True)
    image = models.ImageField(upload_to = 'products/', blank = True, null = True)
    stock = models.PositiveIntegerField(default = 0)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product', args = [self.slug])