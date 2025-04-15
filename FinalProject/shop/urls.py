from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('index/', views.index, name = 'index_alt'),
    path('products/', views.products, name = 'products'),
    path('products/<int:product_id>/', views.product_detail, name = 'product_detail'),
    path('employee/add/', views.add_product, name = 'add_product'),
    path('employee/modify/', views.modify_products, name = 'modify_products'),
    path('employee/edit/<int:product_id>/', views.edit_product, name = 'edit_product'),
    path('employee/delete/<int:product_id>/', views.delete_product, name = 'delete_product'),
    path('category/<int:category_id>/', views.category, name = 'category'),
    path('search/', views.search, name = 'search'),
]