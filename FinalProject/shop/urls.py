from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('products/', views.products),
    path('products/<slug:slug>/', views.Product),
    path('category/<slug:slug>/', views.Category),
]