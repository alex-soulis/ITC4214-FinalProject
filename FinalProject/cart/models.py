from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def __str__(self):
        return sum(item.total_price() for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.product.price * self.quantity
    
ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'orders')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 20, choices = ORDER_STATUS_CHOICES, default = 'pending')
    subtotal = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    shipping = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    tax = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    total = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'order_items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"