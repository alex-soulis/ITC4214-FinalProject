from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name = "Shoes")
        self.product = Product.objects.create(
            name = "Cool Sneakers",
            description = "Cool sneakers",
            price = 99.99,
            brand = "Cool brand",
            color = "Blue",
            stock = 10,
            available = True,
            category = self.category,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Cool Sneakers")

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create (name = "Clothes")
        self.product = Product.objects.create(
            name = "Awesome T-shirt",
            description = "An awesome t-shirt.",
            price = 29.99,
            brand = "AwesomeBrand",
            color = "black",
            stock = 20,
            available = True,
            category = self.category,
        )

    def test_index_view_status_code(self):
        response = self.client.get(reverse('shop:inde'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(reverse('shop:index'))
        self.assertTemplateUsed(response, 'shop/index.html')

    def text_index_view_contains_product(self):
        response = self.client.get(reverse, ('shop:index'))
        self.assertContains(response, "Awesome T-Shirt")