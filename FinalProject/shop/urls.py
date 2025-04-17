from django.urls import path
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
    path('employee/add/', views.add_product, name='add_product'),

    # List all products (only accessible by owners or employees)
    path('employee/list/', views.list_products, name='list_products'),

    # Edit an existing product (only accessible by owners or employees)
    path('employee/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # Delete an existing product (only accessible by owners or employees)
    path('employee/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
