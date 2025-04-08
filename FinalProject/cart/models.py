from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        return sum(item.tota_price() for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField (default = 1)


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.product.price * self.quantity
