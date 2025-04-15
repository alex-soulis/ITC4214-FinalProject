from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart, CartItem

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    context = {'cart': cart, 'cart_items': cart.caritem_set.all()}
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id, available = True)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user = request.user)
    if request.method == "POST":
        cart.cartitem_set.all().delete()
        return redirect('accounts:dashboard')
    context = {'cart': cart}
    return render(request, 'cart/checkout.html', context)