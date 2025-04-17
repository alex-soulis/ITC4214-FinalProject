# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('',                   views.view_cart,      name='cart'),
    path('add/<int:product_id>/',   views.add_to_cart,   name='add'),
    path('update/',            views.update_cart,    name='update'),
    path('remove/<int:item_id>/',   views.remove_from_cart, name='remove'),
    path('checkout/',          views.checkout,       name='checkout'),
]
