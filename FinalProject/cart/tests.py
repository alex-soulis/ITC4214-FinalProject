from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product
from .models import Cart, CartItem

class CartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = 'testpass')
        self.client = Client()
        self.client.login(username = 'testuser', password ='testpass')

        self.category = Category.objects.create(name = "Accessories")
        self.product = Product.objects.create(
            name = "A hat",
            description = "A wow hat",
            price = 19.99,
            brand = "FashionBrand",
            color = "White",
            stock = 5,
            available = True,
            category = self.category,
        )

    def test_view_cart_when_empty(self):
        response = self.client.get(reverse('cart:cart'))
        self.asserEqual(response.status_code, 200)
        self.assertContains(response, "Shopping Cart")

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:add_to_cart', kwargs = {'product_id': self.product.id}))
        cart = Cart.objects.get(user = self.user)
        cart_item = CartItem.objects.get(cart = cart, product = self.product)
        self.assertEqual(cart_item.quantity, 1)