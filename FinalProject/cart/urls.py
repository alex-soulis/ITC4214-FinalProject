from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name = 'cart'),
    path('add/<int:products_id>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove/<int:products_id>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
]