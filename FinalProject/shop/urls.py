from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Homepage - Display featured products and categories
    path('', views.index, name='index'),

    # Products listing - Display all products (with optional filtering)
    path('products/', views.products, name='products'),

    # Product detail - Display details of a specific product
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Category page - Display products in a specific category
    path('category/<int:category_id>/', views.category, name='category'),

    # Search page - Display products based on search query
    path('search/', views.search, name='search'),

    # Add a new product (only accessible by owners or employees)
    path('employees/add/', views.add_product, name='add_product'),

    # List all products (only accessible by owners or employees)
    path('employees/list/', views.list_products, name='list_products'),

    # Edit an existing product (only accessible by owners or employees)
    path('employees/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # Delete an existing product (only accessible by owners or employees)
    path('employees/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('about/', TemplateView.as_view(template_name = 'shop/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name = 'shop/contact.html'), name='contact'),
]